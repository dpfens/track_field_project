from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


# Create your models here.
class Attribute(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_attributes')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_attributes')

    class Meta:
        db_table = 'attribute'


class Entity(models.Model):
    entity_type = models.ForeignKey('EntityType', models.DO_NOTHING)
    name = models.CharField(max_length=150)
    knowledge_graph = models.ForeignKey('utility.KnowledgeGraph', models.DO_NOTHING, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_entities')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_entities')

    class Meta:
        db_table = 'entity'


class EntityAlias(models.Model):
    entity = models.ForeignKey(Entity, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    preferred_indicator = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_entity_aliases',)
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_entity_aliases')

    class Meta:
        db_table = 'entity_alias'


class EntityAttribute(models.Model):
    entity = models.ForeignKey(Entity, models.DO_NOTHING)
    attribute = models.ForeignKey(Attribute, models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_entity_attributes')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_entity_attributes')

    class Meta:
        db_table = 'entity_attribute'
        unique_together = (('entity', 'attribute'),)


class EntityIdentity(models.Model):
    entity = models.ForeignKey(Entity, models.DO_NOTHING)
    identity = models.ForeignKey('Identity', models.DO_NOTHING)
    is_private = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_entity_identities')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_entity_identities')

    class Meta:
        db_table = 'entity_identity'
        unique_together = (('entity', 'identity'),)


class EntityTrait(models.Model):
    entity = models.ForeignKey(Entity, models.DO_NOTHING)
    trait = models.ForeignKey('Trait', models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_entity_traits')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_entity_traits')

    class Meta:
        db_table = 'entity_trait'
        unique_together = (('entity', 'trait'),)


class EntityType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_entity_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_entity_types')

    class Meta:
        db_table = 'entity_type'


class Ethnicity(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_ethnicities')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_ethncities')

    class Meta:
        db_table = 'ethnicity'


class Gender(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_genders')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_genders')

    class Meta:
        db_table = 'gender'


class GoogleLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    iss = models.CharField(max_length=50)
    sub = models.CharField(max_length=50)
    azp = models.CharField(max_length=75)
    aud = models.CharField(max_length=75)
    iat = models.PositiveIntegerField()
    exp = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_google_logins')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_google_logins')

    class Meta:
        db_table = 'google_login'


class Identity(models.Model):
    identity_type = models.ForeignKey('IdentityType', models.DO_NOTHING)
    organization = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    is_private = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('self', models.DO_NOTHING, db_column='created_by', blank=True, null=True, related_name='created_identities')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('self', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_identities')

    class Meta:
        db_table = 'identity'
        unique_together = (('organization', 'identifier'),)


class IdentityAttribute(models.Model):
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    attribute = models.ForeignKey(Attribute, models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='created_identity_attribute')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_identity_attribute')

    class Meta:
        db_table = 'identity_attribute'
        unique_together = (('identity', 'attribute'),)


class IdentityCitizenship(models.Model):
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    country = models.ForeignKey('geography.Country', models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'identity_citizenship'
        unique_together = (('identity', 'country'),)


class IdentityOrganization(models.Model):
    organization_type = models.ForeignKey('OrganizationType', models.DO_NOTHING)
    identity = models.ForeignKey(Identity, models.DO_NOTHING, blank=True, null=True)
    headquarters_location = models.ForeignKey('geography.Location', models.DO_NOTHING, blank=True, null=True, related_name='headquarted_identity_organizations')
    formation_date = models.DateField(blank=True, null=True)
    dissolution_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='created_identity_organization')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_identity_organization')

    class Meta:
        db_table = 'identity_organization'
        unique_together = (('identity', 'organization_type', 'headquarters_location'),)


class IdentityPerson(models.Model):
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    gender = models.ForeignKey(Gender, models.DO_NOTHING)
    race = models.ForeignKey('Race', models.DO_NOTHING, blank=True, null=True, related_name='identity_persons')
    ethnicity = models.ForeignKey(Ethnicity, models.DO_NOTHING, blank=True, null=True)
    given_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='created_identity_person')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_identity_person')

    class Meta:
        db_table = 'identity_person'


class IdentityTrait(models.Model):
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    trait = models.ForeignKey('Trait', models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='created_identity_traits')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_identity_traits')

    class Meta:
        db_table = 'identity_trait'
        unique_together = (('identity', 'trait'),)


class IdentityType(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', blank=True, null=True, related_name='created_identity_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_identity_types')

    class Meta:
        db_table = 'identity_type'


class OrganizationMembership(models.Model):
    organization = models.ForeignKey(Identity, models.DO_NOTHING, related_name='members')
    member = models.ForeignKey(Identity, models.DO_NOTHING, related_name='%(class)s')
    division = models.ForeignKey('athletics.Division', models.DO_NOTHING, null=True, related_name='membership')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'organization_membership'
        unique_together = (('organization', 'member'),)


class OrganizationType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='organization_type_created_by',)
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', related_name='organization_type_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization_type'


class Race(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='created_races')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_races')

    class Meta:
        db_table = 'race'


class Trait(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'trait'


class StagingIdentity(models.Model):
    identity_type = models.ForeignKey('IdentityType', models.DO_NOTHING)
    organization = models.ForeignKey('self', models.DO_NOTHING)
    identifier = models.CharField(max_length=50)
    is_private = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'staging_identity'
        unique_together = (('organization', 'identifier'),)


class StagingIdentityOrganization(models.Model):
    organization_type = models.ForeignKey(OrganizationType, models.DO_NOTHING)
    staging_identity = models.ForeignKey('identity.StagingIdentity', models.DO_NOTHING)
    headquarters_location = models.ForeignKey('geography.Location', models.DO_NOTHING, blank=True, null=True)
    formation_date = models.DateField(blank=True, null=True)
    dissolution_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'staging_identity_organization'
        unique_together = (('staging_identity', 'organization_type', 'headquarters_location'),)


class StagingIdentityPerson(models.Model):
    staging_identity = models.ForeignKey('identity.StagingIdentity', models.DO_NOTHING)
    gender = models.ForeignKey('identity.Gender', models.DO_NOTHING)
    given_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    source = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'staging_identity_person'
