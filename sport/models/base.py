from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from utility.models import base as base_models
from utility.models import attributes as attribute_models


# Create your models here.
class ActivityType(base_models.BaseModel):
    """
    The type of activity

    Example:  Physical, Digital, etc.
    """
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)


class Activity(base_models.BaseAuditModel):
    """
    A given activity

    Example: Athletics, Running, XBox playing, Cross-country skiing
    """
    parent = models.ForeignKey("self", on_delete=models.DO_NOTHING, related_name="%(class)s_children", null=True, blank=True)
    type = models.ForeignKey(ActivityType, on_delete=models.DO_NOTHING)
    is_group = models.BooleanField()
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    wikipedia = models.CharField(max_length=150)
    knowledge_graph = models.OneToOneField('utility.KnowledgeGraph', on_delete=models.DO_NOTHING, blank=True, null=True)


class Annotation(base_models.BaseAuditModel):
    """
    Base definition for an annotation to a given piece of information
    """
    id = models.BigAutoField(primary_key=True)
    annotation_type = models.ForeignKey('AnnotationType', models.DO_NOTHING)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    verified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='verified_by', blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    is_flagged = models.BooleanField(default=False)
    flagged_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='flagged_by', blank=True, null=True, related_name='flagged_annotations')


class AnnotationType(base_models.BaseModel):
    """
    Type of annotation
    """
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)


class AnnotationVote(base_models.BaseModel):
    """
    Records up/down votes of an annotation
    """
    id = models.BigAutoField(primary_key=True)
    annotation = models.ForeignKey(Annotation, models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    up = models.IntegerField()
    down = models.IntegerField()

    class Meta:
        unique_together = (('annotation', 'identity', 'up', 'down'),)


class Area(base_models.BaseModel):
    field_of_play = models.OneToOneField('FieldOfPlay', on_delete=models.DO_NOTHING)


class Category(base_models.BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)


class CategoryHierarchy(base_models.BaseAuditModel):
    parent = models.ForeignKey(Category, models.DO_NOTHING, related_name='children')
    child = models.ForeignKey(Category, models.DO_NOTHING, related_name='parents')

    class Meta:
        unique_together = (('parent', 'child'),)


class CategoryCompetition(base_models.BaseAuditModel):
    category = models.ForeignKey(Category, models.DO_NOTHING)
    competition = models.ForeignKey('Competition', models.DO_NOTHING)

    class Meta:
        unique_together = (('competition', 'category'),)


class Coach(base_models.BaseAuditModel):
    """
    An individual who guide individuals through a process
    """
    coach = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='students')
    student = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='coaches')
    start_date = models.DateField()
    end_date = models.DateField()


class Comment(base_models.BaseAuditModel):
    """
    A comment on a given piece of information

    Differs from an annotation in that Comments are intended for replies and
    discussion
    """
    annotation = models.ForeignKey(Annotation, models.DO_NOTHING)
    reply_to = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)


class GameType(base_models.BaseModel):
    """
    Type of game
    """
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)


class Competition(base_models.BaseAuditModel):
    """
    A base table for competition information
    """
    competition_type = models.ForeignKey('CompetitionType', models.DO_NOTHING)
    event = models.ForeignKey('EventInstance', models.DO_NOTHING, blank=True, null=True)
    division = models.ForeignKey('Division', models.DO_NOTHING, blank=True, null=True)
    activity = models.ForeignKey('Activity', models.DO_NOTHING)
    game = models.ForeignKey('Game', models.DO_NOTHING)
    field_of_play = models.ForeignKey('FieldOfPlay', models.DO_NOTHING, blank=True, null=True)
    scoring_units = models.ForeignKey('utility.Quantity', models.DO_NOTHING, blank=True, null=True)
    objective = models.CharField(max_length=250, null=True, blank=True)
    expected_start = models.DateTimeField(blank=True, null=True)
    actual_start = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    url = models.URLField(null=True, blank=True)
    participants = models.PositiveIntegerField()
    expected_competitiveness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    actual_competitiveness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    expected_eliteness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    actual_eliteness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('athletics.views.competition_details', args=[self.sporting_event.slug, self.slug])

    class Meta:
        unique_together = (('activity', 'field_of_play', 'slug'),)


class CompetitionTrait(attribute_models.BaseTraitModel):
    """
    Characteristics of an competition which do not change over time
    """
    competition = models.ForeignKey(Competition, models.DO_NOTHING)

    class Meta:
        unique_together = (('competition', 'trait'),)


class CompetitionSimilarity(base_models.BaseModel):
    competition = models.OneToOneField(Competition, on_delete=models.DO_NOTHING, related_name='similar_competitions')
    other = models.ForeignKey(Competition, models.DO_NOTHING, related_name='other_similar_competitions')
    value = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        unique_together = (('competition', 'other'),)


class CompetitionType(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=255)


class Disqualification(base_models.BaseAuditModel):
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    class Meta:
        unique_together = (('organization', 'code'),)


class Division(base_models.BaseAuditModel):
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    class Meta:
        unique_together = (('organization', 'name'),)


class Environment(base_models.BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)


class EventType(base_models.BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)


class Event(base_models.BaseAuditModel):
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='child_events')
    event_type = models.ForeignKey('EventType', models.DO_NOTHING)
    environment = models.ForeignKey(Environment, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    expected_competitiveness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    actual_competitiveness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    expected_eliteness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    actual_eliteness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)


class EventAttribute(attribute_models.BaseAttributeModel):
    """
    Characteristics of an competition which can change over time
    """
    event = models.ForeignKey(Event, models.DO_NOTHING)

    class Meta:
        unique_together = (('event', 'attribute'),)


class EventTrait(attribute_models.BaseTraitModel):
    """
    Characteristics of an competition which does not change over time
    """
    event = models.ForeignKey(Event, models.DO_NOTHING)

    class Meta:
        unique_together = (('event', 'trait'),)


class EventInstance(base_models.BaseAuditModel):
    """
    A specific occurrence of an event
    """
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='child_event_instances')
    event = models.ForeignKey(Event, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.PositiveIntegerField()
    website = models.URLField(max_length=255, null=True, blank=True)
    expected_competitiveness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    actual_competitiveness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    expected_eliteness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    actual_eliteness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)


class EventInstanceAttribute(attribute_models.BaseAttributeModel):
    """
    Characteristics of an event instance which can change over time
    """
    event_instance = models.ForeignKey(EventInstance, models.DO_NOTHING)

    class Meta:
        unique_together = (('event_instance', 'attribute'),)


class EventInstanceTrait(attribute_models.BaseTraitModel):
    """
    Characteristics of an event instance which does not change over time
    """
    event_instance = models.ForeignKey(EventInstance, models.DO_NOTHING)

    class Meta:
        unique_together = (('event_instance', 'trait'),)


class FieldOfPlay(base_models.BaseAuditModel):
    """
    A place where an activity can be performed
    """
    id = models.BigAutoField(primary_key=True)
    venue = models.ForeignKey('geography.Venue', models.DO_NOTHING, related_name='fields_of_play')
    name = models.CharField(max_length=50)
    website = models.URLField(max_length=255, null=True, blank=True)
    established = models.DateTimeField(blank=True, null=True)
    retired = models.DateTimeField(blank=True, null=True)


class GameEconomics(base_models.BaseModel):
    """
    The economics of a game

    Example: Zero-sum, positive-sum
    """
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=255)


class Game(base_models.BaseAuditModel):
    """
    Defines a game and how the it functions

    Example: A running race, chess, etc.
    """
    type = models.ForeignKey('GameType', models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    objective = models.TextField()
    scoring_evaluation = models.ForeignKey('ScoringEvaluation', models.DO_NOTHING)
    scoring_mechanism = models.ForeignKey('ScoringMechanism', models.DO_NOTHING)
    scoring_quantity = models.ForeignKey('utility.Quantity', models.DO_NOTHING)
    economics = models.ForeignKey('GameEconomics', models.DO_NOTHING)
    is_perfect_information = models.BooleanField()
    is_symmetric = models.BooleanField()
    is_cooperative = models.BooleanField()
    is_move_by_nature = models.BooleanField()

    class Meta:
        unique_together = (('name', 'scoring_evaluation', 'scoring_mechanism', 'type', 'economics', 'scoring_quantity'),)


class Legitimacies(base_models.BaseModel):
    """
    A table for describing legitimacies/ilegitimacies
    """
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'legitimacies'


class Outcome(base_models.BaseAuditModel):
    """
    A base table for describing the outcome of activities for a given identity
    """
    type = models.ForeignKey('OutcomeType', models.DO_NOTHING, null=True)
    event = models.ForeignKey(EventInstance, models.DO_NOTHING)
    field_of_play = models.ForeignKey(FieldOfPlay, models.DO_NOTHING)
    competition = models.ForeignKey(Competition, models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='performances')
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True, related_name='organization_outcomes')
    place = models.BigIntegerField()
    value = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    state = models.ForeignKey('OutcomeState', models.DO_NOTHING)
    legitimacy = models.ForeignKey(Legitimacies, models.DO_NOTHING)

    class Meta:
        unique_together = (('competition', 'identity', ), )


class OutcomeState(base_models.BaseModel):
    """
    A base table for describing the state of an outcome
    """
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class OutcomeType(base_models.BaseModel):
    """
    A base table for describing a type of outcome
    """
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class OutcomeAgeGroup(base_models.BaseAuditModel):
    id = models.BigIntegerField(primary_key=True)
    outcome = models.OneToOneField(Outcome, models.DO_NOTHING)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()


class OutcomeSimilarity(base_models.BaseModel):
    """
    A table for quantifying the similarity between outcomes
    """
    outcome = models.OneToOneField(Outcome, on_delete=models.DO_NOTHING)
    other = models.ForeignKey(Outcome, models.DO_NOTHING, related_name='%(class)s_other')
    value = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        unique_together = (('outcome', 'other'),)


class OutcomeAttribute(attribute_models.BaseAttributeModel):
    """
    Characteristics of an outcome which can change over time
    """
    outcome = models.ForeignKey(Outcome, models.DO_NOTHING)

    class Meta:
        unique_together = (('outcome', 'attribute'),)


class OutcomeTrait(attribute_models.BaseTraitModel):
    """
    Characteristics of an outcome which does not change over time
    """
    outcome = models.ForeignKey(Outcome, models.DO_NOTHING)

    class Meta:
        unique_together = (('outcome', 'trait'),)


class Review(base_models.BaseAuditModel):
    """
    A base table for storing reviews of an object
    """
    user = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    content_language = models.ForeignKey('geography.Language', models.DO_NOTHING)
    content = models.TextField()


class ReviewFlag(base_models.BaseAuditModel):
    """
    Records when users flag a review
    """
    user = models.OneToOneField('identity.Identity', on_delete=models.DO_NOTHING)
    review = models.ForeignKey(Review, models.DO_NOTHING)
    justification = models.TextField()

    class Meta:
        unique_together = (('user', 'review'),)


class Rule(base_models.BaseAuditModel):
    id = models.PositiveIntegerField(primary_key=True)
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    content = models.TextField()
    proposed_at = models.DateField(blank=True, null=True)
    proposed_by = models.PositiveIntegerField(blank=True, null=True)
    active_at = models.DateField()
    appealed_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Sanctions(base_models.BaseAuditModel):
    substance = models.ForeignKey('Substances', models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    start_violation_date = models.DateField(blank=True, null=True)
    end_violation_date = models.DateField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name_plural = 'sanctions'


class ScoringEvaluation(base_models.BaseModel):
    """
    The method by which a score is evaluated

    Example: Minimum, Maximum
    """
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)


class ScoringMechanism(base_models.BaseModel):
    """
    The method by which a score is evaluated

    Example: Threshold, Endurance
    """
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)


class Series(base_models.BaseAuditModel):
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'series'


class SeriesHierarchy(base_models.BaseModel):
    parent = models.ForeignKey(Series, on_delete=models.DO_NOTHING, related_name='child_series')
    child = models.ForeignKey(Series, models.DO_NOTHING, related_name='parent_series')

    class Meta:
        unique_together = (('parent', 'child'),)


class SeriesCompetition(base_models.BaseAuditModel):
    series = models.OneToOneField(Series, on_delete=models.DO_NOTHING)
    competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (('series', 'competition'),)


class SocialClass(base_models.BaseModel):
    code = models.CharField(unique=True, max_length=8)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'social class'
        verbose_name_plural = 'social classes'


class SocialClassAlias(base_models.BaseModel):
    social_class = models.ForeignKey(SocialClass, models.DO_NOTHING)
    value = models.CharField(max_length=20)

    class Meta:
        unique_together = (('social_class', 'value'),)
        verbose_name_plural = 'social class aliases'


class SponsorshipAthlete(base_models.BaseAuditModel):
    sponsor = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='sponsored_athletes')
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='sponsors')
    amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)


class SponsorshipCompetition(base_models.BaseAuditModel):
    sponsor = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    competition = models.ForeignKey(Competition, models.DO_NOTHING)
    amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)


class Strategy(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "strategies"


class Substances(base_models.BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    wikipedia_url = models.CharField(max_length=100)
    is_banned = models.BooleanField()
    banned_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'substances'


class Surface(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)


class Tier(base_models.BaseModel):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    level = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
