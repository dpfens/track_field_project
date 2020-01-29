from django.contrib.admin.apps import AdminConfig

class DefaultAdminConfig(AdminConfig):
    default_site = 'track_field_project.admin.site.DefaultAdminSite'
