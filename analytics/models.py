from django.db import models

# Create your models here.
class Algorithm(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    type = models.ForeignKey('AlgorithmType', models.DO_NOTHING)
    approach = models.ForeignKey('AlgorithmApproach', models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'algorithm'


class AlgorithmApproach(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'algorithm_approach'


class AlgorithmExecution(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    algorithm = models.ForeignKey(Algorithm, models.DO_NOTHING)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'algorithm_execution'


class AlgorithmParameter(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    algorithm = models.ForeignKey(Algorithm, models.DO_NOTHING)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_optional = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'algorithm_parameter'
        unique_together = (('algorithm', 'name'),)


class AlgorithmParameterValue(models.Model):
    parameter = models.ForeignKey(AlgorithmParameter, models.DO_NOTHING)
    execution = models.ForeignKey(AlgorithmExecution, models.DO_NOTHING)
    value = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'algorithm_parameter_value'
        unique_together = (('execution', 'parameter'),)


class AlgorithmType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
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
    last_modified = models.DateTimeField(blank=True, null=True)
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
    last_modified = models.DateTimeField(blank=True, null=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField()
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by')

    class Meta:
        db_table = 'analytics_browser'

    def __repr__(self):
        return '<%s %s name=%r, version=%r>' % (self.__class__.__name__, id(self), self.name, self.version)

    def __str__(self):
        return str(self.name)


class BrowserFeature(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_browser_features')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_browser_features')

    class Meta:
        db_table = 'analytics_browser_feature'


class BrowserFeatures(models.Model):
    analytics_browser = models.ForeignKey(Browser, models.DO_NOTHING)
    analytics_browser_feature = models.ForeignKey(BrowserFeature, models.DO_NOTHING)
    supported = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_browser_feature_instances')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_browser_feature_instances')

    class Meta:
        db_table = 'analytics_browser_features'
        unique_together = (('analytics_browser', 'analytics_browser_feature'),)


class Device(models.Model):
    device_type = models.ForeignKey('DeviceType', models.DO_NOTHING)
    manufacturer = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'analytics_device'
        unique_together = (('device_type', 'manufacturer', 'name'),)

    def __repr__(self):

        return '<%s %s manufacturer=%r, name=%r>' % (self.__class__.__name__, id(self), self.manufacturer, self.name)

    def __str__(self):
        return str(self.name)


class DeviceType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'analytics_device_type'

    def __repr__(self):
        return '<%s %s name=%r>' % (self.__class__.__name__, id(self), self.name)

    def __str__(self):
        return str(self.name)


class IpAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip_address_type = models.ForeignKey('IpAddressType', models.DO_NOTHING)
    value = models.BinaryField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'analytics_ip_address'


class IpAddressType(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'analytics_ip_address_type'

    def __repr__(self):
        return '<%s %s name=%r>' % (self.__class__.__name__, id(self), self.name)

    def __str__(self):
        return str(self.name)


class OperatingSystem(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    manufacturer = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=25)
    major_version = models.PositiveIntegerField(blank=True, null=True)
    minor_version = models.PositiveIntegerField(blank=True, null=True)
    build_maintenance_version = models.PositiveIntegerField(blank=True, null=True)
    revision_build_version = models.PositiveIntegerField(blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'analytics_operating_system'
        unique_together = (('manufacturer', 'name'),)

    def __repr__(self):
        return '<%s %s manufacturer=%r, name=%r, version=%r>' % (self.__class__.__name__, id(self), self.manufacturer, self.name, self.version)

    def __str__(self):
        output = ''
        if self.manufacturer:
            output += self.manufacturer + ' '
        output += self.name
        if self.version:
            output += ' version: %r' % self.version
        return output


class Referrer(models.Model):
    id = models.BigAutoField(primary_key=True)
    referrer_type = models.ForeignKey('ReferrerType', models.DO_NOTHING)
    value = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'analytics_referrer'


class ReferrerType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'analytics_referrer_type'

    def __repr__(self):
        return '<%s %s name=%r>' % (self.__class__.__name__, id(self), self.name)

    def __str__(self):
        return str(self.name)


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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'analytics_request'


class RequestFeature(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    feature = models.ForeignKey(BrowserFeature, models.DO_NOTHING)
    supported = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_request_browser_features')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_request_browser_features')

    class Meta:
        db_table = 'analytics_request_feature'
        unique_together = (('request', 'feature'),)


class RequestHeaderType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_header_types')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, null=True, blank=True, db_column='last_modified_by', related_name='modified_header_types')

    class Meta:
        db_table = 'analytics_request_header_type'

    def __repr__(self):
        return '<%s %s name=%r>' % (self.__class__.__name__, id(self), self.name)

    def __str__(self):
        return str(self.name)


class RequestHeader(models.Model):
    type = models.ForeignKey(RequestHeaderType, on_delete=models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_headers')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, null=True, blank=True, db_column='last_modified_by', related_name='modified_headers')

    class Meta:
        db_table = 'analytics_request_header'

    def __repr__(self):
        return '<%s %s type=%r, name=%r>' % (self.__class__.__name__, id(self), self.type, self.name)

    def __str__(self):
        return self.name


class RequestHeaderValue(models.Model):
    header = models.ForeignKey(RequestHeader, models.DO_NOTHING)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_header_values')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True, db_column='last_modified_by', related_name='modified_header_values')

    class Meta:
        db_table = 'analytics_request_header_value'
        unique_together = (('header', 'value'),)


class RequestHeaderValues(models.Model):
    request_id = models.BigIntegerField()
    header_value_id = models.PositiveIntegerField()

    class Meta:
        db_table = 'analytics_request_header_values'


class RequestMethod(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=10)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField()
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by')

    class Meta:
        db_table = 'analytics_request_method'

    def __repr__(self):
        return '<%s %s name=%r>' % (self.__class__.__name__, id(self), self.name)

    def __str__(self):
        return str(self.name)


class RequestType(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'analytics_request_type'

    def __repr__(self):
        return '<%s %s name=%r>' % (self.__class__.__name__, id(self), self.name)

    def __str__(self):
        return str(self.name)


class Url(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(unique=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'analytics_url'


class UrlParameter(models.Model):
    name = models.CharField(unique=True, max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_url_parameters')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_url_parameters')

    class Meta:
        db_table = 'analytics_url_parameter'


class UrlParameterValue(models.Model):
    id = models.BigAutoField(primary_key=True)
    parameter = models.ForeignKey(UrlParameter, models.DO_NOTHING)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_url_parameter_values')
    last_modified = models.DateTimeField(auto_now_add=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, null=True, db_column='last_modified_by', related_name='modified_url_parameter_values')

    class Meta:
        db_table = 'analytics_url_parameter_value'
        unique_together = (('parameter', 'value'),)


class UrlParameterValues(models.Model):
    id = models.BigAutoField(primary_key=True)
    request_id = models.BigIntegerField()
    parameter_value_id = models.BigIntegerField()

    class Meta:
        db_table = 'analytics_url_parameter_values'


class UserAgent(models.Model):
    value = models.CharField(unique=True, max_length=250)

    class Meta:
        db_table = 'analytics_user_agent'

    def __repr__(self):
        return '<%s %s value=%r>' % (self.__class__.__name__, id(self), self.value)

    def __str__(self):
        return str(self.value)


class UserLoginArchive(models.Model):
    user = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    login = models.DateTimeField()
    logout = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_login_archive'
