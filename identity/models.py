from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Attribute(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'attribute'


class Entity(models.Model):
    entity_type = models.ForeignKey('EntityType', models.DO_NOTHING)
    name = models.CharField(max_length=150)
    knowledge_graph = models.ForeignKey('utility.KnowledgeGraph', models.DO_NOTHING, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'entity'


class EntityAlias(models.Model):
    entity = models.ForeignKey(Entity, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    preferred_indicator = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    def __str__(self):
        return self.name

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
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'entity_attribute'
        unique_together = (('entity', 'attribute'),)


class EntityIdentity(models.Model):
    entity = models.OneToOneField(Entity, on_delete=models.DO_NOTHING)
    identity = models.OneToOneField('Identity', on_delete=models.DO_NOTHING)
    is_private = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'entity_identity'
        unique_together = (('entity', 'identity'),)


class EntityTrait(models.Model):
    entity = models.ForeignKey(Entity, models.DO_NOTHING)
    trait = models.ForeignKey('Trait', models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'entity_trait'
        unique_together = (('entity', 'trait'),)


class EntityType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'entity_type'


class Gender(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='created_by', related_name='gender_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='gender_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gender'


class Identity(models.Model):
    identity_type = models.ForeignKey('IdentityType', models.DO_NOTHING)
    organization = models.ForeignKey('self', models.DO_NOTHING, null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING, null=True)
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    is_private = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('self', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by', null=True)
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('self', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'identity'
        unique_together = (('organization', 'identifier'),)

    def __str__(self):
        return self.identifier


class IdentityAttribute(models.Model):
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    attribute = models.ForeignKey(Attribute, models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'identity_attribute'
        unique_together = (('identity', 'attribute'),)


class IdentityCitizenship(models.Model):
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    country = models.ForeignKey('geography.Country', models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'identity_citizenship'
        unique_together = (('identity', 'country'),)


class IdentityOrganization(models.Model):
    organization_type = models.ForeignKey('OrganizationType', models.DO_NOTHING)
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    headquarters_location = models.ForeignKey('geography.Location', models.DO_NOTHING, blank=True, null=True)
    formation_date = models.DateField(blank=True, null=True)
    dissolution_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'identity_organization'
        unique_together = (('identity', 'organization_type', 'headquarters_location'),)


class IdentityPerson(models.Model):
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    gender = models.ForeignKey(Gender, models.DO_NOTHING)
    race_id = models.PositiveIntegerField(blank=True, null=True)
    ethnicity_id = models.PositiveIntegerField(blank=True, null=True)
    given_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    source = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'identity_person'


class IdentityTrait(models.Model):
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    trait = models.ForeignKey('Trait', models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'identity_trait'
        unique_together = (('identity', 'trait'),)


class IdentityType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by', null=True)
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey(Identity, models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'identity_type'


class OrganizationMembership(models.Model):
    organization = models.ForeignKey(Identity, models.DO_NOTHING, related_name='members')
    member = models.ForeignKey(Identity, models.DO_NOTHING, related_name='%(class)s')
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
    source = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization_type'


class Trait(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
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
    identity_type = models.ForeignKey('identity.IdentityType', models.DO_NOTHING)
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
    race_id = models.PositiveIntegerField(blank=True, null=True)
    ethnicity_id = models.PositiveIntegerField(blank=True, null=True)
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
