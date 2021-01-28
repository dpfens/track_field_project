from identity import models


class IdentityMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        identity_id = request.session.get('identity')
        if not identity_id:
            if request.user.is_authenticated:
                try:
                    identity = models.Identity.objects.get(user_id=request.user.id)
                except Exception:
                    user_id = request.user.id
                    identity_type = models.IdentityType.objects.get(name='User')
                    identity = models.Identity(identity_type=identity_type, user_id=user_id, is_private=True, identifier=user_id, created_by=None)
                    identity.save()
            else:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    raw_ip_address = x_forwarded_for.split(',')[0]
                else:
                    raw_ip_address = request.META.get('REMOTE_ADDR')
                try:
                    identity = models.Identity.objects.get(identifier=raw_ip_address)
                except Exception:
                    identity_type = models.IdentityType.objects.get(name='Anonymous User')
                    identity = models.Identity(identity_type=identity_type, user_id=None, is_private=True, identifier=raw_ip_address, created_by=None)
                    identity.save()
            request.session['identity'] = identity.id
        else:
            identity = models.Identity.objects.get(pk=identity_id)

        request.identity = identity

        response = self.get_response(request)
        return response
