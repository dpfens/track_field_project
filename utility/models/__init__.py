from django.db import models
from utility.models import base as base_models
from .base import *
from .feedback import *
from .measurement import *
from .attributes import *
from .lookups import *


# Create your models here.
class KnowledgeGraph(base_models.BaseAuditModel):
    id = models.CharField(primary_key=True, max_length=20)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    image_content_url = models.CharField(max_length=250, blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    article_body = models.CharField(max_length=2000)
    wikipedia = models.CharField(max_length=250)

    class Meta:
        db_table = 'knowledge_graph'
