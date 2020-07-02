from django.db import models

# Create your models here.
class Algorithm(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    type = models.ForeignKey('AlgorithmType', models.DO_NOTHING)
    approach = models.ForeignKey('AlgorithmApproach', models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_algorithms')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_algorithms')

    class Meta:
        managed = False
        db_table = 'algorithm'


class AlgorithmApproach(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_algorithm_approaches')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='lasT_modified_algorithm_approaches')

    class Meta:
        managed = False
        db_table = 'algorithm_approach'


class AlgorithmExecution(models.Model):
    algorithm = models.ForeignKey(Algorithm, models.DO_NOTHING)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_algorithm_executions')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_algorithm_parameter_executions')

    class Meta:
        managed = False
        db_table = 'algorithm_execution'


class AlgorithmParameter(models.Model):
    algorithm = models.ForeignKey(Algorithm, models.DO_NOTHING)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_optional = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_algorithm_parameters')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_algorithm_parameters')

    class Meta:
        managed = False
        db_table = 'algorithm_parameter'
        unique_together = (('algorithm', 'name'),)


class AlgorithmParameterValue(models.Model):
    parameter = models.ForeignKey(AlgorithmParameter, models.DO_NOTHING)
    execution = models.ForeignKey(AlgorithmExecution, models.DO_NOTHING)
    value = models.CharField(max_length=14)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_algorithm_parameter_values')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_algorithm_parameter_values')

    class Meta:
        managed = False
        db_table = 'algorithm_parameter_value'
        unique_together = (('execution', 'parameter'),)


class AlgorithmType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_algorithm_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_algorithm_types')

    class Meta:
        managed = False
        db_table = 'algorithm_type'


class AthleteClustering(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    division = models.ForeignKey('athletics.Division', models.DO_NOTHING, blank=True, null=True)
    discipline = models.ForeignKey('athletics.Discipline', models.DO_NOTHING, blank=True, null=True)
    event = models.ForeignKey('athletics.Event', models.DO_NOTHING, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='athlete_clustering_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='atlete_clustering_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'athlete_clustering'


class AthleteClusteringAssignment(models.Model):
    clustering = models.ForeignKey(AthleteClustering, models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='clusters')
    cluster = models.IntegerField()
    membership = models.DecimalField(max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='recent_athlete_clusters')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='recently_modified_athlete_clusters', blank=True, null=True)

    class Meta:
        db_table = 'athlete_clustering_assignment'
        unique_together = (('clustering', 'identity', 'cluster'),)


class Browser(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=250)
    major_version = models.PositiveIntegerField()
    minor_version = models.PositiveIntegerField(blank=True, null=True)
    build_maintenance_version = models.PositiveIntegerField(blank=True, null=True)
    revision_build_version = models.PositiveIntegerField(blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_browsers')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_browsers')

    class Meta:
        managed = False
        db_table = 'analytics_browser'


class BrowserFeature(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_browser_features')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_browser_features')

    class Meta:
        managed = False
        db_table = 'analytics_browser_feature'


class BrowserFeatures(models.Model):
    analytics_browser = models.ForeignKey(Browser, models.DO_NOTHING)
    analytics_browser_feature = models.ForeignKey(BrowserFeature, models.DO_NOTHING)
    supported = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_browser_feature_relationships')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_browser_feature_relationships')

    class Meta:
        managed = False
        db_table = 'analytics_browser_features'
        unique_together = (('analytics_browser', 'analytics_browser_feature'),)


class Device(models.Model):
    device_type = models.ForeignKey('DeviceType', models.DO_NOTHING)
    manufacturer = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_devices')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_devices')

    class Meta:
        managed = False
        db_table = 'analytics_device'
        unique_together = (('device_type', 'manufacturer', 'name'),)


class DeviceType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_device_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_device_types')

    class Meta:
        managed = False
        db_table = 'analytics_device_type'


class IpAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip_address_type = models.ForeignKey('IpAddressType', models.DO_NOTHING)
    value = models.CharField(max_length=32)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_ip_addresses')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_ip_addresses')

    class Meta:
        managed = False
        db_table = 'analytics_ip_address'
        unique_together = (('ip_address_type', 'value'),)


class IpAddressType(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_ip_address_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_ip_address_types')

    class Meta:
        managed = False
        db_table = 'analytics_ip_address_type'


class OperatingSystem(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    manufacturer = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=25)
    major_version = models.PositiveIntegerField(blank=True, null=True)
    minor_version = models.PositiveIntegerField(blank=True, null=True)
    build_maintenance_version = models.PositiveIntegerField(blank=True, null=True)
    revision_build_version = models.PositiveIntegerField(blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_operating_systems')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_operating_systems')

    class Meta:
        managed = False
        db_table = 'analytics_operating_system'
        unique_together = (('manufacturer', 'name'),)


class Referrer(models.Model):
    id = models.BigAutoField(primary_key=True)
    referrer_type = models.ForeignKey('ReferrerType', models.DO_NOTHING)
    value = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_referrers')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_referrers')

    class Meta:
        managed = False
        db_table = 'analytics_referrer'


class ReferrerType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_referrer_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_referrer_types')

    class Meta:
        managed = False
        db_table = 'analytics_referrer_type'


class Request(models.Model):
    id = models.BigAutoField(primary_key=True)
    request_type_id = models.PositiveIntegerField()
    identity_id = models.PositiveIntegerField(blank=True, null=True)
    referrer_id = models.BigIntegerField(blank=True, null=True)
    method_id = models.PositiveIntegerField()
    ip_address_id = models.BigIntegerField()
    device_id = models.PositiveIntegerField(blank=True, null=True)
    browser_id = models.PositiveSmallIntegerField(blank=True, null=True)
    url_id = models.BigIntegerField()
    user_agent_id = models.PositiveIntegerField()
    requested_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'analytics_request'


class RequestFeature(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    feature = models.ForeignKey(BrowserFeature, models.DO_NOTHING)
    supported = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_request_features')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_request_features')

    class Meta:
        managed = False
        db_table = 'analytics_request_feature'
        unique_together = (('request', 'feature'),)


class RequestHeader(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    type = models.ForeignKey('RequestHeaderType', models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_request_headers')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_request_headers')

    class Meta:
        managed = False
        db_table = 'analytics_request_header'


class RequestHeaderType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_request_header_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_request_header_types')

    class Meta:
        managed = False
        db_table = 'analytics_request_header_type'


class RequestHeaderValue(models.Model):
    header = models.ForeignKey(RequestHeader, models.DO_NOTHING)
    value = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_request_header_values')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_request_header_values')

    class Meta:
        managed = False
        db_table = 'analytics_request_header_value'
        unique_together = (('header', 'value'),)


class RequestHeaderValues(models.Model):
    request_id = models.BigIntegerField()
    header_value_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'analytics_request_header_values'


class RequestMethod(models.Model):
    name = models.CharField(unique=True, max_length=10)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_request_methods')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_request_methods')

    class Meta:
        managed = False
        db_table = 'analytics_request_method'


class RequestType(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_request_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_request_types')

    class Meta:
        managed = False
        db_table = 'analytics_request_type'


class Url(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(unique=True, max_length=250)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_urls')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_urls')

    class Meta:
        managed = False
        db_table = 'analytics_url'


class UrlParameter(models.Model):
    name = models.CharField(unique=True, max_length=25)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_url_parameters')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_url_parameters')

    class Meta:
        managed = False
        db_table = 'analytics_url_parameter'


class UrlParameterValue(models.Model):
    id = models.BigAutoField(primary_key=True)
    parameter = models.ForeignKey(UrlParameter, models.DO_NOTHING)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_url_parameter_values')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_url_parameter_values')

    class Meta:
        managed = False
        db_table = 'analytics_url_parameter_value'
        unique_together = (('parameter', 'value'),)


class UrlParameterValues(models.Model):
    id = models.BigAutoField(primary_key=True)
    request_id = models.BigIntegerField()
    parameter_value_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'analytics_url_parameter_values'


class UserAgent(models.Model):
    value = models.CharField(unique=True, max_length=250)

    class Meta:
        managed = False
        db_table = 'analytics_user_agent'
