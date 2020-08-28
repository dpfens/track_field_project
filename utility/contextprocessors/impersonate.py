from django.contrib.auth import get_user_model
from utility.middleware.impersonate import ImpersonationMiddleware
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

User = get_user_model()


def impersonation(request):
    session_key = ImpersonationMiddleware.session_key
    impersonate_parameter = ImpersonationMiddleware.impersonate_parameter
    unimpersonate_parameter = ImpersonationMiddleware.unimpersonate_parameter

    allowed_to_impersonate = ImpersonationMiddleware.is_authorized_to_impersonate(request.user)
    is_impersonating = session_key in request.session
    impersonated_user = None
    unimpersonate_parameters = {}

    if is_impersonating:
        impersonated_user_id = request.session[session_key]
        impersonated_user = User.objects.get(id=impersonated_user_id)
        unimpersonate_parameters = dict(**request.GET)
        unimpersonate_parameters.pop(impersonate_parameter, None)
        unimpersonate_parameters[unimpersonate_parameter] = True
    elif allowed_to_impersonate and not is_impersonating:
        impersonate_parameters = dict(**request.GET)
        impersonate_parameters.pop(unimpersonate_parameter, None)

    if unimpersonate_parameters:
        unimpersonate_parameters = urlencode(unimpersonate_parameters)

    return {
        'impersonated_user': impersonated_user,
        'is_impersonating': is_impersonating,
        'unimpersonate_parameters': unimpersonate_parameters,
        'impersonate_parameter': impersonate_parameter,
        'allowed_to_impersonate': allowed_to_impersonate
    }
