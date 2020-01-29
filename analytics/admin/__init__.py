from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from analytics import models


@admin.register(models.Browser, site=advanced_admin)
class BrowserAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')

@admin.register(models.Device, site=advanced_admin)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'device_type')
    list_filter = ('manufacturer', 'device_type')

@admin.register(models.DeviceType, site=advanced_admin)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.RequestHeader, site=advanced_admin)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name', 'type')

@admin.register(models.RequestHeaderType, site=advanced_admin)
class HeaderTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.IpAddressType, site=advanced_admin)
class IpAddressTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.OperatingSystem, site=advanced_admin)
class OperatingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'version')

@admin.register(models.ReferrerType, site=advanced_admin)
class ReferrerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(models.RequestMethod, site=advanced_admin)
class RequestMethodAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.RequestType, site=advanced_admin)
class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.UserAgent, site=advanced_admin)
class UserAgentAdmin(admin.ModelAdmin):
    search_fields = ('name', )
