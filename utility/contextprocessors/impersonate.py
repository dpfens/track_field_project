from utility.middleware.impersonate import ImpersonationMiddleware
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def impersonation(request):
    """
    This context processor is used in conjunctiion with the
    administer.middleware.impersonate.ImpersonationMiddleware to provide the
    required template variables to power the GUI to help non-technical users
    manage impersonation.
    """
    impersonate_parameter = ImpersonationMiddleware.impersonate_parameter
    unimpersonate_parameter = ImpersonationMiddleware.unimpersonate_parameter

    is_impersonated = request.impersonation.is_impersonated

    unimpersonate_parameters = {}

    if is_impersonated:
        unimpersonate_parameters = dict(**request.GET)
        unimpersonate_parameters.pop(impersonate_parameter, None)
        unimpersonate_parameters[unimpersonate_parameter] = True

    if unimpersonate_parameters:
        unimpersonate_parameters = urlencode(unimpersonate_parameters)

    return {
        'unimpersonate_parameters': unimpersonate_parameters,
        'impersonate_parameter': impersonate_parameter,
    }
