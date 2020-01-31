from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from identity import models


@admin.register(models.Attribute, site=advanced_admin)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.Entity, site=advanced_admin)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity_type')

@admin.register(models.EntityAlias, site=advanced_admin)
class EntityAliasAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity', 'preferred_indicator')

@admin.register(models.EntityAttribute, site=advanced_admin)
class EntityAttributeAdmin(admin.ModelAdmin):
    list_display = ('entity', 'attribute', 'value', 'is_primary')

@admin.register(models.EntityIdentity, site=advanced_admin)
class EntityIdentityAdmin(admin.ModelAdmin):
    list_display = ('entity', 'identity', 'is_private')

@admin.register(models.EntityTrait, site=advanced_admin)
class EntityTraitAdmin(admin.ModelAdmin):
    list_display = ('entity', 'trait', 'value', 'is_primary')

@admin.register(models.EntityType, site=advanced_admin)
class EntityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.Gender, site=advanced_admin)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.Identity, site=advanced_admin)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'identity_type', 'organization')

@admin.register(models.IdentityType, site=advanced_admin)
class IdentityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.IdentityAttribute, site=advanced_admin)
class IdentityAttributeAdmin(admin.ModelAdmin):
    list_display = ('identity', 'attribute', 'value', 'is_primary')

@admin.register(models.IdentityTrait, site=advanced_admin)
class IdentityTraitAdmin(admin.ModelAdmin):
    list_display = ('identity', 'trait', 'value', 'is_primary')

@admin.register(models.IdentityCitizenship, site=advanced_admin)
class IdentityCitizenshipAdmin(admin.ModelAdmin):
    list_display = ('identity', 'country', 'start_date', 'end_date')

@admin.register(models.IdentityOrganization, site=advanced_admin)
class IdentityOrganizationAdmin(admin.ModelAdmin):
    list_display = ('identity', 'organization_type', 'headquarters_location')

@admin.register(models.IdentityPerson, site=advanced_admin)
class IdentityPersonAdmin(admin.ModelAdmin):
    list_display = ('identity', 'gender', 'given_name', 'last_name')

@admin.register(models.OrganizationType, site=advanced_admin)
class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.Trait, site=advanced_admin)
class TraitAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.StagingIdentity, site=advanced_admin)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'identity_type', 'organization')

@admin.register(models.StagingIdentityPerson, site=advanced_admin)
class StagingIdentityPersonAdmin(admin.ModelAdmin):
    list_display = ('staging_identity', 'gender', 'given_name', 'last_name')

@admin.register(models.StagingIdentityOrganization, site=advanced_admin)
class StagingIdentityOrganizationAdmin(admin.ModelAdmin):
    list_display = ('staging_identity', 'organization_type', 'headquarters_location')
