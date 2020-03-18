from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from identity import models

READONLY_FIELDS = ('created_at', 'created_by', 'last_modified_at', 'last_modified_by')


@admin.register(models.Attribute, site=advanced_admin)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.Entity, site=advanced_admin)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity_type')
    readonly_fields = READONLY_FIELDS

@admin.register(models.EntityAlias, site=advanced_admin)
class EntityAliasAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity', 'preferred_indicator')
    readonly_fields = READONLY_FIELDS

@admin.register(models.EntityAttribute, site=advanced_admin)
class EntityAttributeAdmin(admin.ModelAdmin):
    list_display = ('entity', 'attribute', 'value', 'is_primary')
    readonly_fields = READONLY_FIELDS

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("start_date (%s) must be before end_date (%s)" % (self.start_date, self.end_date))
        return self.cleaned_data

@admin.register(models.EntityIdentity, site=advanced_admin)
class EntityIdentityAdmin(admin.ModelAdmin):
    list_display = ('entity', 'identity', 'is_private')
    readonly_fields = READONLY_FIELDS

@admin.register(models.EntityTrait, site=advanced_admin)
class EntityTraitAdmin(admin.ModelAdmin):
    list_display = ('entity', 'trait', 'value', 'is_primary')
    readonly_fields = READONLY_FIELDS

@admin.register(models.EntityType, site=advanced_admin)
class EntityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.Gender, site=advanced_admin)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.Identity, site=advanced_admin)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'identity_type', 'organization')
    readonly_fields = READONLY_FIELDS

@admin.register(models.IdentityType, site=advanced_admin)
class IdentityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.IdentityAttribute, site=advanced_admin)
class IdentityAttributeAdmin(admin.ModelAdmin):
    list_display = ('identity', 'attribute', 'value', 'is_primary')
    readonly_fields = READONLY_FIELDS

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("start_date (%s) must be before end_date (%s)" % (self.start_date, self.end_date))
        return self.cleaned_data

@admin.register(models.IdentityTrait, site=advanced_admin)
class IdentityTraitAdmin(admin.ModelAdmin):
    list_display = ('identity', 'trait', 'value', 'is_primary')
    readonly_fields = READONLY_FIELDS

@admin.register(models.IdentityCitizenship, site=advanced_admin)
class IdentityCitizenshipAdmin(admin.ModelAdmin):
    list_display = ('identity', 'country', 'start_date', 'end_date')

@admin.register(models.IdentityOrganization, site=advanced_admin)
class IdentityOrganizationAdmin(admin.ModelAdmin):
    list_display = ('identity', 'organization_type', 'headquarters_location')
    readonly_fields = READONLY_FIELDS

@admin.register(models.IdentityPerson, site=advanced_admin)
class IdentityPersonAdmin(admin.ModelAdmin):
    list_display = ('identity', 'gender', 'given_name', 'last_name')
    readonly_fields = READONLY_FIELDS

@admin.register(models.OrganizationType, site=advanced_admin)
class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.Trait, site=advanced_admin)
class TraitAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.StagingIdentity, site=advanced_admin)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'identity_type', 'organization')
    readonly_fields = READONLY_FIELDS

@admin.register(models.StagingIdentityPerson, site=advanced_admin)
class StagingIdentityPersonAdmin(admin.ModelAdmin):
    list_display = ('staging_identity', 'gender', 'given_name', 'last_name')
    readonly_fields = READONLY_FIELDS

@admin.register(models.StagingIdentityOrganization, site=advanced_admin)
class StagingIdentityOrganizationAdmin(admin.ModelAdmin):
    list_display = ('staging_identity', 'organization_type', 'headquarters_location')
    readonly_fields = READONLY_FIELDS
