
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

from utility.models import base as base_models
from utility.models import attributes as attribute_models


User = get_user_model()


# Create your models here.
class Entity(base_models.BaseAuditModel):
    """
    Stores the immutable information about an entity.

    Entities can have multiple identities, which can change over time.
    """
    id = models.BigAutoField(primary_key=True)
    entity_type = models.ForeignKey('EntityType', models.DO_NOTHING)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    knowledge_graph = models.ForeignKey('utility.KnowledgeGraph', models.DO_NOTHING, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = (('entity_type', 'slug'), )

    def save(self, *args, **kwargs):
        if not self.slug:
            raw_slug = slugify(self.name)
            count = 1
            slug = raw_slug
            while Entity.objects.filter(slug=slug).exists():
                slug = '%s-%s' % (raw_slug, count)
                count = count + 1
            self.slug = slug
        super(Entity, self).save(*args, **kwargs)


class EntityAlias(base_models.BaseAuditModel):
    """
    Alias names of an entity
    """
    id = models.BigAutoField(primary_key=True)
    entity = models.ForeignKey(Entity, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    preferred_indicator = models.BooleanField()


class EntityAttribute(attribute_models.BaseAttributeModel):
    """
    Characteristics of an entity which can change over time
    """
    entity = models.ForeignKey(Entity, models.DO_NOTHING)

    class Meta:
        unique_together = (('entity', 'attribute'),)


class EntityIdentity(base_models.BaseAuditModel):
    """
    Identities of an entity.  Also indicated if the identity is public or not
    """
    id = models.BigAutoField(primary_key=True)
    entity = models.ForeignKey(Entity, models.DO_NOTHING)
    identity = models.ForeignKey('Identity', models.DO_NOTHING)
    is_private = models.BooleanField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (('entity', 'identity'),)


class EntityTrait(base_models.BaseAuditModel):
    """
    Characteristics of an entity which do not change over time
    """
    id = models.BigAutoField(primary_key=True)
    entity = models.ForeignKey(Entity, models.DO_NOTHING)
    trait = models.ForeignKey('utility.Trait', models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.BooleanField()

    class Meta:
        unique_together = (('entity', 'trait'),)


class EntityType(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class Ethnicity(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class Gender(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)


class GoogleLogin(base_models.BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    iss = models.CharField(max_length=50)
    sub = models.CharField(max_length=50)
    azp = models.CharField(max_length=75)
    aud = models.CharField(max_length=75)
    iat = models.PositiveIntegerField()
    exp = models.PositiveIntegerField()


class Identity(base_models.BaseAuditModel):
    """
    Identity of an entity

    Indicates if the identity is private or not
    """
    id = models.BigAutoField(primary_key=True)
    identity_type = models.ForeignKey('IdentityType', models.DO_NOTHING)
    organization = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    is_primary = models.BooleanField()
    is_private = models.BooleanField()
    is_active = models.BooleanField()
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('identity.views.identity_details', args=[self.slug])

    class Meta:
        unique_together = (('organization', 'identifier'),)


class IdentityAttribute(attribute_models.BaseAttributeModel):
    """
    Characteristics of an identity which can change over time
    """
    identity = models.ForeignKey(Identity, models.DO_NOTHING)

    class Meta:
        unique_together = (('identity', 'attribute'),)


class IdentityCitizenship(base_models.BaseModel):
    """
    Citizenship of an identity over time
    """
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    country = models.ForeignKey('geography.Country', models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = (('identity', 'country'),)


class IdentityOrganization(base_models.BaseAuditModel):
    """
    Information about an Organization
    """
    id = models.BigAutoField(primary_key=True)
    organization_type = models.ForeignKey('OrganizationType', models.DO_NOTHING)
    identity = models.ForeignKey(Identity, models.DO_NOTHING, blank=True, null=True)
    headquarters_location = models.ForeignKey('geography.Location', models.DO_NOTHING, blank=True, null=True, related_name='headquarted_identity_organizations')
    formation_date = models.DateField(blank=True, null=True)
    dissolution_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('identity', 'organization_type', 'headquarters_location'),)


class IdentityPerson(base_models.BaseAuditModel):
    """
    Information about a Person
    """
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(Identity, models.DO_NOTHING)
    gender = models.ForeignKey(Gender, models.DO_NOTHING)
    race = models.ForeignKey('Race', models.DO_NOTHING, blank=True, null=True, related_name='identity_persons')
    ethnicity = models.ForeignKey(Ethnicity, models.DO_NOTHING, blank=True, null=True)
    given_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)


class IdentityTeam(base_models.BaseAuditModel):
    """
    Information about a Team
    """
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(Identity, models.DO_NOTHING, related_name='identity_teams')
    team_type = models.ForeignKey('TeamType', models.DO_NOTHING)


class IdentityTrait(attribute_models.BaseTraitModel):
    """
    Characteristics of an identity which do not change over time
    """
    identity = models.ForeignKey(Identity, models.DO_NOTHING)

    class Meta:
        unique_together = (('identity', 'trait'),)


class IdentityType(base_models.BaseModel):
    """
    Type of identity

    Example. Individual, Organization, etc.
    """
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)


class OrganizationMembership(base_models.BaseAuditModel):
    """
    Information about membership to an organization
    """
    organization = models.ForeignKey(Identity, models.DO_NOTHING, related_name='members')
    member = models.ForeignKey(Identity, models.DO_NOTHING, related_name='%(class)s')
    division = models.ForeignKey('sport.Division', models.DO_NOTHING, null=True, related_name='membership')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (('organization', 'member'),)


class OrganizationType(base_models.BaseModel):
    """
    Type of Organization

    Example: LLC, Federation, Association, Corporation
    """
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Race(base_models.BaseModel):
    """
    Information about human races
    """
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class TeamType(base_models.BaseModel):
    """
    Types of teams:

    Example: Relay, etc.
    """
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
