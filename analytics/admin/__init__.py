from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from analytics import models


@admin.register(models.Browser, site=advanced_admin)
class BrowserAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Device, site=advanced_admin)
class DeviceAdmin(admin.ModelAdmin):
    pass

@admin.register(models.DeviceType, site=advanced_admin)
class DeviceTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.RequestHeader, site=advanced_admin)
class HeaderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RequestHeaderType, site=advanced_admin)
class HeaderTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.OperatingSystem, site=advanced_admin)
class OperatingSystemAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ReferrerType, site=advanced_admin)
class ReferrerAdmin(admin.ModelAdmin):
    pass

@admin.register(models.RequestMethod, site=advanced_admin)
class RequestMethodAdmin(admin.ModelAdmin):
    pass

@admin.register(models.RequestType, site=advanced_admin)
class RequestTypeAdmin(admin.ModelAdmin):
    pass
