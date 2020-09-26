from django.db import models
from utility.models import base as base_models


# Create your models here.
class Algorithm(base_models.BaseModel):
    type = models.ForeignKey('AlgorithmType', models.DO_NOTHING)
    approach = models.ForeignKey('AlgorithmApproach', models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class AlgorithmApproach(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class AlgorithmExecution(base_models.BaseModel):
    algorithm = models.ForeignKey(Algorithm, models.DO_NOTHING)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)


class AlgorithmParameter(base_models.BaseModel):
    algorithm = models.ForeignKey(Algorithm, models.DO_NOTHING)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_optional = models.BooleanField()

    class Meta:
        unique_together = (('algorithm', 'name'),)


class AlgorithmParameterValue(base_models.BaseModel):
    parameter = models.ForeignKey(AlgorithmParameter, models.DO_NOTHING)
    execution = models.ForeignKey(AlgorithmExecution, models.DO_NOTHING)
    value = models.CharField(max_length=14)

    class Meta:
        unique_together = (('execution', 'parameter'),)


class AlgorithmType(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class AthleteClustering(base_models.BaseModel):
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    division = models.ForeignKey('sport.Division', models.DO_NOTHING, blank=True, null=True)
    activity = models.ForeignKey('sport.Activity', models.DO_NOTHING, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField()


class AthleteClusteringAssignment(base_models.BaseModel):
    clustering = models.ForeignKey(AthleteClustering, models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='clusters')
    cluster = models.IntegerField()
    membership = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        unique_together = (('clustering', 'identity', 'cluster'),)
