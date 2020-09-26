from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from utility import models
from utility.models import measurement as measurement_models


READONLY_FIELDS = ('created_at', 'last_modified_at')


@admin.register(models.Attribute, site=advanced_admin)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS


@admin.register(models.Trait, site=advanced_admin)
class TraitAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS


@admin.register(models.KnowledgeGraph, site=advanced_admin)
class KnowledgeGraphAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


@admin.register(measurement_models.Quantity, site=advanced_admin)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    # list_select_related = ('si_unit', )
    readonly_fields = READONLY_FIELDS
    ordering = ('name', )


@admin.register(measurement_models.Unit, site=advanced_admin)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit_system')
    list_select_related = ('quantity', 'unit_system')
    readonly_fields = READONLY_FIELDS
    ordering = ('name', )


@admin.register(measurement_models.UnitSystem, site=advanced_admin)
class UnitSystemAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS
    ordering = ('name', )
