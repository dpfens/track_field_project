from django.db import models
from utility.models import base as base_models


class Quantity(base_models.BaseModel):
    """
    Quantities that can be measured

    Ex. Distance, Mass, Voltage, etc.
    """
    name = models.CharField(unique=True, max_length=150)
    description = models.TextField()
    wikipedia_url = models.CharField(max_length=150)
    symbol = models.CharField(max_length=10)
    si_unit = models.ForeignKey('Unit', models.DO_NOTHING, null=True, related_name='si_quantity')

    def __str__(self):
        return self.name


class Unit(base_models.BaseModel):
    """
    A Unit for measuring a Quantity in a Unit System

    Example: Meters, Feet, Miles, Seconds, Ohms, etc.
    """
    unit_system = models.ForeignKey('UnitSystem', models.DO_NOTHING)
    quantity = models.ForeignKey(Quantity, models.DO_NOTHING)
    name = models.CharField(max_length=150)
    description = models.TextField()
    acronym = models.CharField(max_length=5)
    abbreviation = models.CharField(max_length=10)
    wikipedia_url = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('unit_system', 'quantity', 'name'),)


class UnitSystem(base_models.BaseModel):
    """
    Systems of measuring quantities in units

    examples: English, Metric, etc.
    """
    name = models.CharField(unique=True, max_length=150)
    description = models.TextField()
    wikipedia_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name
