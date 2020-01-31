from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from utility import models


@admin.register(models.KnowledgeGraph, site=advanced_admin)
class KnowledgeGraphAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


@admin.register(models.Quantity, site=advanced_admin)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Unit, site=advanced_admin)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_system', 'quantity')


@admin.register(models.UnitSystem, site=advanced_admin)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', )
