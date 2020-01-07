import logging
from identity import models


logger = logging.getLogger(__name__)


def identity(request):
    if request.user.is_authenticated:
        try:
            identity = models.Identity.objects.get(user_id=request.user.id)
        except Exception as e:
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
    request.identity = identity
    return dict()
