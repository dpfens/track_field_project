from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from utility.models import base as base_models


class Ownership(base_models.BaseAuditModel):
    owned_at = models.DateTimeField(blank=True, null=True)
    owned_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True, related_name='ownerships')

    def change_ownership(self, owner):
        now = datetime.now()
        has_existing_owner = self.owned_at and self.owned_by
        self.owned_by = owner
        self.owned_at = now

        if has_existing_owner:
            if self.owned_by == owner:
                raise ValueError('%r already owned by %r' % (self, owner))
            previous_owner = self.owned_by
            ownership_start_date = self.owned_at
            Provenance.objects.create(item=self, identity=previous_owner, start_date=ownership_start_date, end_date=now)

    class Meta:
        abstract = True


class Provenance(base_models.BaseAuditModel):
    """
    History of ownership of an item
    """
    item_type = models.ForeignKey(ContentType, models.DO_NOTHING)
    item = GenericForeignKey('content_type', 'object_id')
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='provenance')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Responsibility(base_models.LookupModel, base_models.BaseModel):
    pass


class Delegation(base_models.BaseAuditModel):
    delegator = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='delegations')
    delegatee = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='delegation_assignments')
    responsibility = models.ForeignKey(Responsibility, models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
