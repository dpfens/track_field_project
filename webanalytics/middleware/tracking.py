import logging
from analytics import models
from datetime import datetime
import ipaddress
from track_field_project import settings
from django.core.exceptions import MiddlewareNotUsed


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        if settings.DEBUG:
            raise MiddlewareNotUsed('In DEBUG mode')

    def __call__(self, request):
        do_not_track = request.headers.get('DNT', 0)
        request.do_not_track = do_not_track

        if request.do_not_track:
            return

        identity = request.identity
        now = datetime.now()

        # fetch/add method
        try:
            method = models.RequestMethod.objects.get(name=request.method)
        except Exception as e:
            method = models.RequestMethod(name=request.method)
            method.save()

        # fetch/add IP Address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            raw_ip_address = x_forwarded_for.split(',')[0]
        else:
            raw_ip_address = request.META.get('REMOTE_ADDR')

        try:
            ip_address = ipaddress.ipaddress(raw_ip_address)
        except Exception:
            logger.warning('IP Address is not valid: %r', raw_ip_address)
            ip_address_type_name = 'Invalid'
        else:
            if isinstance(ip_address, ipaddress.IPv6Address):
                ip_address_type_name = 'IPv6'
            else:
                ip_address_type_name = 'IPv4'
        ip_address_type = models.IpAddressType.objects.get(name=ip_address_type_name)
        raw_ip_address = bytes(raw_ip_address, 'utf8')
        try:
            ip_address = models.IpAddress.objects.get(ip_address_type=ip_address_type, value=raw_ip_address)
        except Exception:
            ip_address = models.IpAddress(ip_address_type=ip_address_type, value=raw_ip_address)
            ip_address.save()


        # fetch/add UserAgent
        raw_user_agent = request.META['HTTP_USER_AGENT']
        try:
            user_agent = models.UserAgent.objects.get(value=raw_user_agent)
        except Exception as e:
            user_agent = models.UserAgent(value=raw_user_agent)
            user_agent.save()

        # fetch/add Device
        device = request.user_agent.device
        device_family = device.family

        if request.user_agent.is_mobile:
            device_type = 'Mobile'
        elif request.user_agent.is_tablet:
            device_type = 'Tablet'
        elif request.user_agent.is_pc:
            device_type = 'PC'
        elif request.user_agent.is_bot:
            device_type = 'Bot'
        else:
            device_type = 'Unknown'

        try:
            device_type = models.DeviceType.objects.get(name=device_type)
        except Exception as e:
            logger.warning('%r is not a known device Type: %r', user_agent, e)
            device_type = models.DeviceType(name=device_family, description='')
            device_type.save()

        try:
            device = models.Device.objects.get(device_type=device_type, name=device_family)
        except Exception as e:
            logger.warning('%r is not a known device_family: %r', device_family, e)
            device = models.Device(device_type=device_type, name=device_family)
            device.save()

        # fetch/add Browser
        try:
            browser = models.Browser.objects.get(name=request.user_agent.browser.family, version=request.user_agent.browser.version_string)
        except Exception as e:
            versions = dict()
            version_keys = ['major_version', 'minor_version', 'build_maintenance_version', 'revision_build_version']
            for version_type, version in zip(version_keys, request.user_agent.browser.version):
                versions[version_type] = version
            browser = models.Browser(name=request.user_agent.browser.family, version=request.user_agent.browser.version_string, description='', created_by_id=identity, **versions)
            browser.save()

        # fetch/add Operating System
        try:
            operating_system = models.OperatingSystem.objects.get(name=request.user_agent.os.family, version=request.user_agent.os.version_string)
        except Exception as e:
            versions = dict()
            version_keys = ['major_version', 'minor_version', 'build_maintenance_version', 'revision_build_version']
            for version_type, version in zip(version_keys, request.user_agent.os.version):
                versions[version_type] = version
            operating_system = models.OperatingSystem(name=request.user_agent.os.family, version=request.user_agent.os.version_string, **versions)
            operating_system.save()

        raw_url = request.build_absolute_uri('?')
        try:
            url = models.Url.objects.get(value=raw_url)
        except Exception as e:
            url = models.Url(value=raw_url, created_by_id=identity)
            url.save()

        # fetch/add Referrer
        raw_referrer = request.META.get('HTTP_REFERER')
        if raw_referrer:
            try:
                referrer = models.Referrer.objects.get(value=raw_referrer)
            except Exception as e:
                if 'https' in raw_referrer.lower():
                    raw_referrer_type = 'HTTPS'
                else:
                    raw_referrer_type = 'HTTP'
                try:
                    referrer_type = models.ReferrerType.objects.get(name=raw_referrer_type)
                except Exception as e:
                    referrer_type = models.ReferrerType(name=raw_referrer_type)
                    referrer_type.save()
                referrer = models.Referrer(value=raw_referrer, referrer_type=referrer_type)
                referrer.save()
            referrer_id = referrer.id
        else:
            referrer_id = None

        # fetch/add request type
        if request.is_secure:
            raw_request_type = 'HTTPS'
        else:
            raw_request_type = 'HTTP'
        try:
            request_type = models.RequestType.objects.get(name=raw_request_type)
        except Exception as e:
            request_type = models.RequestType(name=raw_request_type, description='')
            request_type.save()

        request_instance = models.Request(request_type_id=request_type.id, identity_id=identity, referrer_id=referrer_id, method_id=method.id, ip_address_id=ip_address.id, device_id=device.id, browser_id=browser.id, url_id=url.id, user_agent_id=user_agent.id, requested_at=now)
        request_instance.save()

        response = self.get_response(request)
        return response
