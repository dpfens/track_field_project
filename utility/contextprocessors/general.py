from track_field_project import settings

def general_info(request):
    return {
        'debug': settings.DEBUG,
        'GTM_ID': settings.GTM_ID,
        'google_site_verification_code': settings.google_site_verification_code
    }
