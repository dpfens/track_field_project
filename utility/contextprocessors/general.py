from track_field_project import settings


def general_info(request):
    raw_save_data = request.headers.get('Save-Data')
    save_data = raw_save_data == 'on'

    device_memory = request.headers.get('Device-Memory', 1)

    return {
        'debug': settings.DEBUG,
        'save_data': save_data,
        'device_memory': device_memory,
        'GTM_ID': settings.GTM_ID,
        'google_site_verification_code': settings.google_site_verification_code
    }


def device_info(request):
    raw_save_data = request.headers.get('Save-Data')
    save_data = raw_save_data == 'on'
    device_memory = request.headers.get('Device-Memory', 1)
    return {
        'save_data': save_data,
        'device_memory': device_memory,
    }
