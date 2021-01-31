from django.db import models
from utility.models import base as base_models


dimension_choices = (
    ('E', 'Event'),
    ('F', 'Event Instance'),
    ('I', 'Identity'),
    ('C', 'Competition'),
    ('H', 'Heat'),
    ('O', 'Outcome'),
    ('S', 'Split')
)


class Attribute(base_models.BaseModel):
    """
    A table for storing attributes, which are characteristics whose values can
    change over time
    """
    dimension = models.CharField(max_length=5, choices=dimension_choices)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class Trait(base_models.BaseModel):
    """
    A table for storing attributes, which are characteristics whose values will
    not change over time
    """
    dimension = models.CharField(max_length=5, choices=dimension_choices)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BaseAttributeModel(base_models.BaseAuditModel):
    """
    A table for storing characteristics about an item that can change over time
    """
    id = models.BigAutoField(primary_key=True)
    attribute = models.ForeignKey('utility.Attribute', models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.BooleanField()
    is_verified = models.BooleanField()
    is_private = models.BooleanField()
    is_internal = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class BaseTraitModel(base_models.BaseAuditModel):
    """
    A table for storing characteristics about an item that does not change
    over time
    """
    id = models.BigAutoField(primary_key=True)
    trait = models.ForeignKey('utility.Trait', models.DO_NOTHING)
    value = models.CharField(max_length=13)
    is_primary = models.BooleanField()
    is_verified = models.BooleanField()
    is_private = models.BooleanField()
    is_internal = models.BooleanField(default=False)

    class Meta:
        abstract = True
