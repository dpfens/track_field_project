from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from webanalytics import models

READONLY_FIELDS = ('created_at', 'last_modified_at',)

@admin.register(models.Browser, site=advanced_admin)
class BrowserAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')
    readonly_fields = READONLY_FIELDS

@admin.register(models.Device, site=advanced_admin)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'device_type')
    list_filter = ('manufacturer', 'device_type')
    readonly_fields = READONLY_FIELDS

@admin.register(models.DeviceType, site=advanced_admin)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.RequestHeader, site=advanced_admin)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name', 'type')
    readonly_fields = READONLY_FIELDS

@admin.register(models.RequestHeaderType, site=advanced_admin)
class HeaderTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.IpAddressType, site=advanced_admin)
class IpAddressTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.OperatingSystem, site=advanced_admin)
class OperatingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'version')
    readonly_fields = READONLY_FIELDS

@admin.register(models.ReferrerType, site=advanced_admin)
class ReferrerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.RequestMethod, site=advanced_admin)
class RequestMethodAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.RequestType, site=advanced_admin)
class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    readonly_fields = READONLY_FIELDS

@admin.register(models.UserAgent, site=advanced_admin)
class UserAgentAdmin(admin.ModelAdmin):
    search_fields = ('name', )
