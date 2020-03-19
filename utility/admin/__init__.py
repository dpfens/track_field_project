from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from utility import models


READONLY_FIELDS = ('created_at', 'created_by', 'last_modified_at', 'last_modified_by')


@admin.register(models.KnowledgeGraph, site=advanced_admin)
class KnowledgeGraphAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


@admin.register(models.Quantity, site=advanced_admin)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    # list_select_related = ('si_unit', )
    readonly_fields = READONLY_FIELDS
    ordering = ('name', )


@admin.register(models.Unit, site=advanced_admin)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit_system')
    list_select_related = ('quantity', 'unit_system')
    readonly_fields = READONLY_FIELDS
    ordering = ('name', )


@admin.register(models.UnitSystem, site=advanced_admin)
class UnitSystemAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS
    ordering = ('name', )
