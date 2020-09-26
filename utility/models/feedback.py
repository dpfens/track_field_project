# Create your models here.
from django.db import models
from utility.models import base as base_models


class Feedback(base_models.BaseModel):
    identity = models.ForeignKey('identity.Identity', on_delete=models.DO_NOTHING, null=True)
    email_address = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=250)
    feedback_type = models.ForeignKey('FeedbackType', on_delete=models.CASCADE)
    content = models.TextField()


class FeedbackType(base_models.BaseModel):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
