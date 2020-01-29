from django.contrib.admin import AdminSite


class DefaultAdminSite(AdminSite):
    site_header = 'Track & Field Administration'
    site_title = 'Track & Field Administration'
    index_title = 'Track & Field Administration'


class AdvancedAdminSite(AdminSite):
    site_header = 'Advanced Track & Field Administration'
    site_title = 'Advanced Track & Field Administration'
    index_title = 'Advanced Track & Field Administration'


advanced_admin = AdvancedAdminSite(name='power_user_admin')
