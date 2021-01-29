from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()


class Impersonation(object):
    """
    An attribute of the request object, contains information describing the
    current state of impersonation.

    Attributes:
        is_authorized (bool):  Indicates if the real user is allowed to impersonate another user
        is_impersonated (bool):  Indicates if the current user is impersonated by another
        impersonating_user_banner_id (string):  Only set if is_impersonated is True,
            the banner ID of the user who is impersonating another
        impersonating_user (User):  Only set if is_impersonated is True,
            the User instance of the user who is impersonating the impersonated_user
        impersonated_user_banner_id (string):  Only set if is_impersonated is True,
            the banner ID of the user who is being impersonated by impersonating_user
        impersonated_user (User):  Only set if is_impersonated is True,
            the User instance of the user who is being impersonated by impersonating_user
    """

    def __init__(self, is_authorized, is_impersonated, impersonating_user_banner_id, impersonating_user, impersonated_user_banner_id, impersonated_user):
        self.is_authorized = is_authorized
        self.is_impersonated = is_impersonated
        self.impersonating_user_banner_id = impersonating_user_banner_id
        self.impersonating_user = impersonating_user
        self.impersonated_user_banner_id = impersonated_user_banner_id
        self.impersonated_user = impersonated_user

    def __repr__(self):
        return '<%s is_authorized=%r, is_impersonated=%r>' % (self.__class__.__name__, self.is_authorized, self.is_impersonated)


class ImpersonationMiddleware(object):
    """
    Allows a superuser or members of an "Impersonator" group
    to impersonate another user by adding the impersonate parameter query
    parameter to a URL with a valid Banner ID,  which would change the
    current user to the user with the specific Banner ID.  Subsequent requests
    to the server will be as the impersonated user until the unimpersonate
    parameter is included in a request.

    The request.user is replaced with an instance of the requested user to be
    impersonated.  The actual user is stored in the
    request.impersonation.impersonating_user attribute.

    If the user does not exist, a 500 Error will be raised saying that a
    user does not exist with the specified Banner ID.

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
    impersonate_parameter = '__impersonate'
    unimpersonate_parameter = '__unimpersonate'

    impersonated_session_key = 'impersonated_user_id'
    impersonated_banner_session_key = 'impersonated_user_banner_id'

    impersonating_session_key = 'impersonating_user_id'
    impersonating_banner_session_key = 'impersonating_user_banner_id'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @classmethod
    def is_authorized_to_impersonate(cls, user):
        if user.is_superuser:
            return True
        return user.groups.filter(name=cls.group).exists()

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
                impersonated_user_bannerid = request.GET[self.impersonate_parameter]
                impersonated_user_attribute = models.CustomUserAttributes.objects.filter(attribute='bannerid', value=impersonated_user_bannerid).first()

                if not impersonated_user_attribute:
                    message = 'No user with the Banner ID %s exists in this application.  Please try another Banner ID' % impersonated_user_bannerid
                    return HttpResponse(message, status=500)

                impersonated_user = impersonated_user_attribute.user

                # determine if the actual user is allowed to impersonate the user they requested
                if impersonated_user.is_superuser and not request.user.is_superuser:
                    message = 'Non-superusers are not allowed to impersonate superusers.  Please try a Banner ID of a non-superuser'
                    return HttpResponse(message, status=500)

                impersonating_user_attribute = request.user.attributes.filter(attribute='bannerid').first()
                if not impersonating_user_attribute:
                    message = 'You do not have a bannerid and cannot impersonate'
                    return HttpResponse(message, status=500)

                impersonating_user_banner_id = impersonating_user_attribute.value
                request.session[self.impersonated_session_key] = impersonated_user.id
                request.session[self.impersonated_banner_session_key] = impersonated_user_bannerid

                request.session[self.impersonating_session_key] = request.user.id
                request.session[self.impersonating_banner_session_key] = impersonating_user_banner_id
            elif has_unimpersonate_parameter and self.impersonated_session_key in request.session:
                del request.session[self.impersonated_session_key]
                del request.session[self.impersonated_banner_session_key]

                del request.session[self.impersonating_session_key]
                del request.session[self.impersonating_banner_session_key]

        is_impersonated = self.impersonated_session_key in request.session
        impersonation = Impersonation(is_authorized, is_impersonated, None, request.user, None, None)
        if is_impersonated:
            impersonated_user_id = request.session[self.impersonated_session_key]
            impersonated_user = User.objects.get(id=impersonated_user_id)

            request.user = impersonation.impersonated_user = impersonated_user
            impersonation.impersonated_user_banner_id = request.session[self.impersonated_banner_session_key]
            impersonation.impersonating_user_banner_id = request.session[self.impersonating_banner_session_key]
        request.impersonation = impersonation
