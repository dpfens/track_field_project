from django.db import models

from utility.models import base as base_models
from utility.models import attributes as attribute_models


class AnnotationAttempt(base_models.BaseAuditModel):
    attempt = models.ForeignKey('Attempt', models.DO_NOTHING)
    sequence = models.PositiveIntegerField()


class AnnotationSplit(base_models.BaseAuditModel):
    race_outcome = models.ForeignKey('RaceOutcome', models.DO_NOTHING)
    cumulative_distance = models.DecimalField(max_digits=10, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=3)
    cumulative_time = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.DecimalField(max_digits=10, decimal_places=3)


class Attempt(base_models.BaseAuditModel):
    type = models.ForeignKey('AttemptType', models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.CASCADE)
    outcome = models.ForeignKey('Outcome', models.CASCADE)
    sequence = models.PositiveIntegerField()
    state = models.ForeignKey('AttemptState', models.DO_NOTHING)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    wind = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)


class AttemptAttribute(attribute_models.BaseAttributeModel):
    attempt = models.ForeignKey(Attempt, models.DO_NOTHING)

    class Meta:
        unique_together = (('attempt', 'attribute'),)


class AttemptTrait(attribute_models.BaseTraitModel):
    attempt = models.ForeignKey(Attempt, models.DO_NOTHING)

    class Meta:
        unique_together = (('attempt', 'trait'),)


class AttemptState(base_models.BaseModel):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)


class AttemptType(base_models.BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)


class CompetitionRace(base_models.BaseAuditModel):
    competition = models.OneToOneField('Competition', on_delete=models.DO_NOTHING)
    course = models.OneToOneField('Course', on_delete=models.DO_NOTHING)
    timing_system = models.ForeignKey('TimingSystem', models.DO_NOTHING, blank=True, null=True)
    start_interval = models.PositiveIntegerField()
    distance = models.FloatField()
    distance_unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    mode = models.ForeignKey('Mode', models.DO_NOTHING)
    is_stage = models.BooleanField(default=False)


class CompetitionRaceHurdles(base_models.BaseAuditModel):
    competition = models.OneToOneField('Competition', on_delete=models.DO_NOTHING)
    height = models.DecimalField(max_digits=4, decimal_places=3)
    unit = models.ForeignKey('utility.Unit', on_delete=models.DO_NOTHING)


class CompetitionWeight(base_models.BaseAuditModel):
    competition = models.OneToOneField('Competition', on_delete=models.DO_NOTHING)
    value = models.DecimalField(max_digits=5, decimal_places=3)
    unit = models.ForeignKey('utility.Unit', on_delete=models.DO_NOTHING)


class Course(base_models.BaseAuditModel):
    course_type = models.ForeignKey('CourseType', models.DO_NOTHING)
    field_of_play = models.ForeignKey('FieldOfPlay', models.DO_NOTHING)
    surface = models.ForeignKey('Surface', models.DO_NOTHING, null=True, blank=True)
    distance = models.DecimalField(max_digits=12, decimal_places=3)
    distance_unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    start_location = models.ForeignKey('geography.Location', models.DO_NOTHING, blank=True, null=True, related_name='course_starts')
    finish_location = models.ForeignKey('geography.Location', models.DO_NOTHING, blank=True, null=True, related_name='course_finishes')


class CourseAttribute(attribute_models.BaseAttributeModel):
    course = models.ForeignKey(Course, models.DO_NOTHING)

    class Meta:
        unique_together = (('course', 'attribute'),)


class CourseTrait(attribute_models.BaseTraitModel):
    course = models.ForeignKey(Course, models.DO_NOTHING)

    class Meta:
        unique_together = (('course', 'trait'),)


class CourseGrade(base_models.BaseAuditModel):
    course = models.ForeignKey(Course, models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    degrees = models.FloatField(blank=True, null=True)
    start = models.DecimalField(max_digits=10, decimal_places=2)
    end = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (('course', 'sequence'),)


class CourseSimilarity(base_models.BaseModel):
    course = models.OneToOneField(Course, on_delete=models.DO_NOTHING, related_name='course_similarities')
    other = models.ForeignKey(Course, models.DO_NOTHING, related_name='other_course_similarities')
    value = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        unique_together = (('course', 'other'),)


class CourseSurface(base_models.BaseAuditModel):
    course = models.ForeignKey(Course, models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    surface = models.ForeignKey('Surface', models.DO_NOTHING)
    start = models.DecimalField(max_digits=10, decimal_places=2)
    end = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (('course', 'sequence'),)


class CourseType(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class Heat(base_models.BaseAuditModel):
    competition = models.ForeignKey('Competition', models.CASCADE)
    tier = models.ForeignKey('Tier', models.DO_NOTHING)
    is_overall = models.BooleanField()
    name = models.CharField(max_length=50)


class Mode(base_models.BaseModel):
    """
    Mode of transportation

    Ex. Running, Swimming, Cycling, Walking, Wheelchair, Race Car, etc.
    """
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RaceOutcome(base_models.BaseAuditModel):
    outcome = models.OneToOneField('Outcome', models.CASCADE)
    heat = models.ForeignKey(Heat, models.CASCADE, null=True)
    mode = models.ForeignKey(Mode, models.DO_NOTHING)
    social_class = models.ForeignKey('SocialClass', models.DO_NOTHING, blank=True, null=True)
    squad = models.CharField(max_length=1, blank=True, null=True)
    points = models.SmallIntegerField(blank=True, null=True)
    bib = models.PositiveIntegerField(blank=True, null=True)
    reaction_time = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    wind = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    unattached = models.BooleanField()
    state = models.ForeignKey('RaceOutcomeState', models.DO_NOTHING)
    strategy = models.ForeignKey('Strategy', models.DO_NOTHING, blank=True, null=True)


class RaceOutcomeState(base_models.BaseModel):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RelayOrder(base_models.BaseAuditModel):
    race_outcome = models.ForeignKey('RaceOutcome', models.CASCADE)
    relay = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relay_orders')
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relay_member_orders')
    sequence = models.PositiveSmallIntegerField()
    distance = models.PositiveIntegerField()

    class Meta:
        unique_together = (('race_outcome', 'identity', 'sequence'),)
        verbose_name_plural = 'relay orders'


class RelayMember(base_models.BaseAuditModel):
    relay = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relay_members')
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relays')
    is_alternate = models.BooleanField()

    class Meta:
        unique_together = (('relay', 'identity'),)
        verbose_name_plural = 'relay members'


class Seed(base_models.BaseAuditModel):
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    competition = models.ForeignKey('Competition', models.DO_NOTHING)
    seed_method = models.ForeignKey('SeedMethod', models.DO_NOTHING)
    value = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        unique_together = (('competition', 'identity', 'seed_method'),)


class SeedMethod(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Split(base_models.BaseAuditModel):
    race_outcome = models.OneToOneField(RaceOutcome, on_delete=models.DO_NOTHING)
    competitor = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    mode = models.ForeignKey(Mode, models.DO_NOTHING)
    cumulative_distance = models.DecimalField(max_digits=10, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=3)
    cumulative_time = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.DecimalField(max_digits=10, decimal_places=3)


class SplitAttribute(attribute_models.BaseAttributeModel):
    split = models.ForeignKey(Split, models.DO_NOTHING)

    class Meta:
        unique_together = (('split', 'attribute'),)


class SplitTrait(attribute_models.BaseTraitModel):
    split = models.ForeignKey(Split, models.DO_NOTHING)

    class Meta:
        unique_together = (('split', 'trait'),)


class TimingSystem(base_models.BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
