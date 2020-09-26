from django.db import models
from utility.models import base as base_models


class Browser(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=250)
    major_version = models.PositiveSmallIntegerField()
    minor_version = models.PositiveSmallIntegerField(blank=True, null=True)
    build_maintenance_version = models.PositiveSmallIntegerField(blank=True, null=True)
    revision_build_version = models.PositiveSmallIntegerField(blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'analytics_browser'


class BrowserFeature(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=250)

    class Meta:
        db_table = 'analytics_browser_feature'


class BrowserFeatures(base_models.BaseModel):
    analytics_browser = models.ForeignKey(Browser, models.DO_NOTHING)
    analytics_browser_feature = models.ForeignKey(BrowserFeature, models.DO_NOTHING)
    supported = models.BooleanField()

    class Meta:
        db_table = 'analytics_browser_features'
        unique_together = (('analytics_browser', 'analytics_browser_feature'),)


class Device(base_models.BaseModel):
    device_type = models.ForeignKey('DeviceType', models.DO_NOTHING)
    manufacturer = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'analytics_device'
        unique_together = (('device_type', 'manufacturer', 'name'),)


class DeviceType(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)

    class Meta:
        db_table = 'analytics_device_type'


class IpAddress(base_models.BaseModel):
    id = models.BigAutoField(primary_key=True)
    ip_address_type = models.ForeignKey('IpAddressType', models.DO_NOTHING)
    value = models.CharField(max_length=32)

    class Meta:
        db_table = 'analytics_ip_address'
        unique_together = (('ip_address_type', 'value'),)


class IpAddressType(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)

    class Meta:
        db_table = 'analytics_ip_address_type'


class OperatingSystem(base_models.BaseModel):
    manufacturer = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=25)
    major_version = models.PositiveIntegerField(blank=True, null=True)
    minor_version = models.PositiveIntegerField(blank=True, null=True)
    build_maintenance_version = models.PositiveIntegerField(blank=True, null=True)
    revision_build_version = models.PositiveIntegerField(blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'analytics_operating_system'
        unique_together = (('manufacturer', 'name'),)


class Referrer(base_models.BaseModel):
    id = models.BigAutoField(primary_key=True)
    referrer_type = models.ForeignKey('ReferrerType', models.DO_NOTHING)
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'analytics_referrer'


class ReferrerType(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)

    class Meta:
        db_table = 'analytics_referrer_type'


class Request(base_models.BaseModel):
    id = models.BigAutoField(primary_key=True)
    request_type_id = models.PositiveSmallIntegerField()
    identity_id = models.BigIntegerField(blank=True, null=True)
    referrer_id = models.BigIntegerField(blank=True, null=True)
    method_id = models.PositiveSmallIntegerField()
    ip_address_id = models.BigIntegerField()
    device_id = models.PositiveIntegerField(blank=True, null=True)
    browser_id = models.PositiveSmallIntegerField(blank=True, null=True)
    url_id = models.BigIntegerField()
    user_agent_id = models.PositiveIntegerField()
    requested_at = models.DateTimeField()

    class Meta:
        db_table = 'analytics_request'


class RequestFeature(base_models.BaseModel):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    feature = models.ForeignKey(BrowserFeature, models.DO_NOTHING)
    supported = models.BooleanField()

    class Meta:
        db_table = 'analytics_request_feature'
        unique_together = (('request', 'feature'),)


class RequestHeader(base_models.BaseModel):
    type = models.ForeignKey('RequestHeaderType', models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'analytics_request_header'


class RequestHeaderType(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'analytics_request_header_type'


class RequestHeaderValue(base_models.BaseModel):
    header = models.ForeignKey(RequestHeader, models.DO_NOTHING)
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'analytics_request_header_value'
        unique_together = (('header', 'value'),)


class RequestHeaderValues(base_models.BaseModel):
    request_id = models.BigIntegerField()
    header_value_id = models.PositiveIntegerField()

    class Meta:
        db_table = 'analytics_request_header_values'


class RequestMethod(base_models.BaseModel):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=10)
    description = models.CharField(max_length=250)

    class Meta:
        db_table = 'analytics_request_method'


class RequestType(base_models.BaseModel):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)

    class Meta:
        db_table = 'analytics_request_type'


class Url(base_models.BaseModel):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(unique=True, max_length=250)

    class Meta:
        db_table = 'analytics_url'


class UrlParameter(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=25)

    class Meta:
        db_table = 'analytics_url_parameter'


class UrlParameterValue(base_models.BaseModel):
    id = models.BigAutoField(primary_key=True)
    parameter = models.ForeignKey(UrlParameter, models.DO_NOTHING)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'analytics_url_parameter_value'
        unique_together = (('parameter', 'value'),)


class UrlParameterValues(base_models.BaseModel):
    id = models.BigAutoField(primary_key=True)
    request_id = models.BigIntegerField()
    parameter_value_id = models.BigIntegerField()

    class Meta:
        db_table = 'analytics_url_parameter_values'


class UserAgent(base_models.BaseModel):
    value = models.CharField(unique=True, max_length=250)

    class Meta:
        db_table = 'analytics_user_agent'
