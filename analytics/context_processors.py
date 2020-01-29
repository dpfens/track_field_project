import logging
from analytics import models
from datetime import datetime
import ipaddress
import urllib.parse as urlparse
from urllib.parse import parse_qs


logger = logging.getLogger(__name__)


def log_request(request):
    if not request.identity:
        return
    now = datetime.now()

    # fetch/add method
    try:
        method = models.RequestMethod.objects.get(name=request.method)
    except Exception as e:
        method = models.RequestMethod(name=request.method, created_by=request.identity)
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
        ip_address = models.IpAddress(ip_address_type=ip_address_type, value=raw_ip_address, created_by=request.identity)
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
        device_type = models.DeviceType(name=device_family, description='', created_by=request.identity)
        device_type.save()

    try:
        device = models.Device.objects.get(device_type=device_type, name=device_family)
    except Exception as e:
        logger.warning('%r is not a known device_family: %r', device_family, e)
        device = models.Device(device_type=device_type, name=device_family, created_by=request.identity)
        device.save()

    # fetch/add Browser
    try:
        browser = models.Browser.objects.get(name=request.user_agent.browser.family, version=request.user_agent.browser.version_string)
    except Exception as e:
        versions = dict()
        version_keys = ['major_version', 'minor_version', 'build_maintenance_version', 'revision_build_version']
        for version_type, version in zip(version_keys, request.user_agent.browser.version):
            versions[version_type] = version
        browser = models.Browser(name=request.user_agent.browser.family, version=request.user_agent.browser.version_string, description='', created_by=request.identity, **versions)
        browser.save()

    # fetch/add Operating System
    try:
        operating_system = models.OperatingSystem.objects.get(name=request.user_agent.os.family, version=request.user_agent.os.version_string)
    except Exception as e:
        versions = dict()
        version_keys = ['major_version', 'minor_version', 'build_maintenance_version', 'revision_build_version']
        for version_type, version in zip(version_keys, request.user_agent.os.version):
            versions[version_type] = version
        operating_system = models.OperatingSystem(name=request.user_agent.os.family, version=request.user_agent.os.version_string, created_by=request.identity, **versions)
        operating_system.save()

    raw_url = request.build_absolute_uri('?')
    try:
        url = models.Url.objects.get(value=raw_url)
    except Exception as e:
        url = models.Url(value=raw_url, created_by=request.identity)
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
                referrer_type = models.ReferrerType(name=raw_referrer_type, created_by=request.identity)
                referrer_type.save()
            referrer = models.Referrer(value=raw_referrer, referrer_type=referrer_type, created_by=request.identity)
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
        request_type = models.RequestType(name=raw_request_type, description='', created_by=request.identity)
        request_type.save()

    request_instance = models.Request(request_type_id=request_type.id, identity_id=request.identity.id, referrer_id=referrer_id, method_id=method.id, ip_address_id=ip_address.id, device_id=device.id, browser_id=browser.id, url_id=url.id, user_agent_id=user_agent.id, requested_at=now, created_by=request.identity.id)
    request_instance.save()

    raw_url = request.build_absolute_uri()
    parsed = urlparse.urlparse(raw_url)
    query_parameters = parse_qs(parsed.query)
    for parameter, value in query_parameters.items():
        try:
            url_parameter = models.UrlParameter.objects.get(name=parameter)
        except Exception:
            url_parameter = models.UrlParameter(name=parameter, created_by=request.identity)
            url_parameter.save()

        try:
            url_parameter_value = models.UrlParameterValue.objects.get(parameter_id=url_parameter.id, value=value)
        except Exception:
            url_parameter_value = models.UrlParameterValue(parameter=url_parameter, value=value, created_by=request.identity)
            url_parameter_value.save()

        url_parameter_value_instance = models.UrlParameterValues(request_id=request_instance.id, parameter_value_id=url_parameter_value.id)
        url_parameter_value_instance.save()

    for header_name, value in request.headers.items():
        try:
            request_header = models.RequestHeader.objects.get(name=header_name)
        except Exception:
            request_header_type = models.RequestHeaderType.objects.get(name='Other')
            request_header = models.RequestHeader(type=request_header_type, name=header_name, created_by=request.identity)
            request_header.save()

        try:
            request_header_value = models.RequestHeaderValue.objects.get(header=request_header, value=value)
        except Exception:
            request_header_value = models.RequestHeaderValue(header=request_header, value=value, created_by=request.identity)
            request_header_value.save()

        url_request_header_instance = models.RequestHeaderValues(request_id=request_instance.id, header_value_id=request_header_value.id)
        url_request_header_instance.save()
    return dict()
