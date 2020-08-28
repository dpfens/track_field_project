from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()


class ImpersonationMiddleware(object):
    """
    Allows a superuser, staff, or members of an "Impersonator" group
    to impersonate another user by adding the impersonate parameter query
    parameter to a URL with a valid User ID,  which would change the
    current user to the user with the specific User ID.  Subsequent requests
    to the server will be as the impersonated user until the unimpersonate
    parameter is included in a request.

    If the user does not exist, a 500 Error will be raised saying that a
    user does not exist with the specified username/ID.

    Non-superusers are not allowed to impersonate superusers, regardless of if
    they are a member of the impersonator group

    To revert back to the original user, add the __unimpersonate parameter
    to the URL.  The
    middleware will check for the existence of the __unimpersonate parameter
    so the value of the parameter is irrelevant.

    The parameters used to trigger impersonation/unimpersonation can be
    changed below, as well as the group authorized to impersonate users, and
    the session key used to store the impersonated user's ID.  The parameter
    name changes will be reflected in middleware error messages.
    """
    group = 'Impersonator'
    is_staff = True
    impersonate_parameter = '__impersonate'
    unimpersonate_parameter = '__unimpersonate'

    session_key = 'impersonated_user_id'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @classmethod
    def is_authorized_to_impersonate(cls, user):
        if user.is_superuser:
            return True
        if cls.is_staff and user.is_staff:
            return True
        if cls.group:
            return user.groups.filter(name=cls.group).exists()
        return False

    def process_view(self, request, view_func, view_args, view_kwargs):
        has_impersonate_parameter = self.impersonate_parameter in request.GET
        has_unimpersonate_parameter = self.unimpersonate_parameter in request.GET

        is_impersonation_request = has_impersonate_parameter or has_unimpersonate_parameter
        is_authorized = self.is_authorized_to_impersonate(request.user)

        if is_impersonation_request and is_authorized:
            if has_impersonate_parameter and has_unimpersonate_parameter:
                message = 'Parameters found for both impersonation and unimpersonation.  Please provide either the impersonate parameter (%r) or the unimpersonate parameter (%r)' % (self.impersonate_parameter, self.unimpersonate_parameter)
                return HttpResponse(message, status=500)

            if has_impersonate_parameter:
                user_id = request.GET[self.impersonate_parameter]
                queryset = User.objects.filter(pk=user_id) | User.objects.filter(username=user_id)
                user = queryset.first()

                if not user:
                    message = 'No user with the username/id %r exists in this application.  Please try another username/id' % user_id
                    return HttpResponse(message, status=500)

                impersonated_user = user

                # determine if the actual user is allowed to impersonate the user they requested
                if impersonated_user.is_superuser and not request.user.is_superuser:
                    message = 'Non-superusers are not allowed to impersonate superusers.  Please try the username/id of a non-superuser'
                    return HttpResponse(message, status=500)

                request.session[self.session_key] = impersonated_user.id
            elif has_unimpersonate_parameter and self.session_key in request.session:
                del request.session[self.session_key]

        if self.session_key in request.session:
            impersonated_user_id = request.session[self.session_key]
            request.user = User.objects.get(id=impersonated_user_id)
