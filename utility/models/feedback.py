# Create your models here.
from django.db import models
from utility.models import base as base_models


class Feedback(base_models.BaseModel):
    identity = models.ForeignKey('identity.Identity', on_delete=models.DO_NOTHING, null=True)
    email_address = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=250)
    content = models.TextField()
    is_addressed = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_resolved and not self.is_addressed:
            self.is_addressed = True
        super().save(*args, **kwargs)


class FeedbackLabel(base_models.BaseModel):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    is_internal = models.BooleanField(default=False)


class FeedbackLabels(base_models.BaseAuditModel):
    feedback = models.ForeignKey(Feedback, models.CASCADE)
    label = models.ForeignKey(FeedbackLabel, models.CASCADE)
    is_internal = models.BooleanField(default=False)
