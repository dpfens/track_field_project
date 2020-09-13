from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.
class Annotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    annotation_type = models.ForeignKey('AnnotationType', models.DO_NOTHING)
    content = models.TextField()
    is_public = models.BooleanField()
    is_verified = models.BooleanField()
    verified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='verified_by', blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_annotations')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_annotations')

    class Meta:
        db_table = 'annotation'


class AnnotationAttempt(models.Model):
    attempt = models.ForeignKey('Attempt', models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_sequential_attempt_annotations')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_sequential_attempt_annotations')

    class Meta:
        db_table = 'annotation_attempt'


class AnnotationSplit(models.Model):
    race_outcome = models.ForeignKey('RaceOutcome', models.DO_NOTHING)
    cumulative_distance = models.DecimalField(max_digits=10, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=3)
    cumulative_time = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_annotation_splits')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_annotation_splits')

    class Meta:
        db_table = 'annotation_split'


class AnnotationType(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_annotation_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_annotation_types')

    class Meta:
        db_table = 'annotation_type'


class AnnotationVote(models.Model):
    id = models.BigAutoField(primary_key=True)
    annotation = models.ForeignKey(Annotation, models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    up = models.IntegerField()
    down = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_annotation_votes')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_annotation_votes')

    class Meta:
        db_table = 'annotation_vote'
        unique_together = (('annotation', 'identity', 'up', 'down'),)


class Area(models.Model):
    field_of_play = models.OneToOneField('FieldOfPlay', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_areas')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_areas')

    class Meta:
        db_table = 'area'


class Attempt(models.Model):
    type = models.ForeignKey('AttemptType', models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.CASCADE)
    outcome = models.ForeignKey('Outcome', models.CASCADE)
    sequence = models.PositiveIntegerField()
    state = models.ForeignKey('AttemptState', models.DO_NOTHING)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    wind = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_attempts')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_attempts')

    class Meta:
        db_table = 'attempt'


class AttemptState(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_attempt_states')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_attempt_states')

    class Meta:
        db_table = 'attempt_state'


class AttemptType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_attempt_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_attempt_types')

    class Meta:
        db_table = 'attempt_type'


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_categories')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_categories')

    class Meta:
        db_table = 'category'


class CategoryHierarchy(models.Model):
    parent = models.ForeignKey(Category, models.DO_NOTHING, related_name='children')
    child = models.ForeignKey(Category, models.DO_NOTHING, related_name='parents')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_category_hierarchies')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_category_hierarchies')

    class Meta:
        db_table = 'category_hierarchy'
        unique_together = (('parent', 'child'),)


class CategorySportingEvent(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING)
    sporting_event = models.ForeignKey('SportingEvent', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_category_sporting_events')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_category_sporting_events')

    class Meta:
        db_table = 'category_sporting_event'
        unique_together = (('sporting_event', 'category'),)


class Coach(models.Model):
    coach = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='athletes')
    athlete = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='coaches')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_coaches')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_coaches')

    class Meta:
        db_table = 'coach'


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    reply_to_comment = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    is_flagged = models.BooleanField()
    flagged_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='flagged_by', blank=True, null=True, related_name='flagged_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_comments')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_comments')

    class Meta:
        db_table = 'comment'


class Competition(models.Model):
    competition_type = models.ForeignKey('CompetitionType', models.DO_NOTHING)
    sporting_event = models.ForeignKey('SportingEvent', models.DO_NOTHING)
    division = models.ForeignKey('Division', models.DO_NOTHING, blank=True, null=True)
    sport = models.ForeignKey('Sport', models.DO_NOTHING)
    field_of_play = models.ForeignKey('FieldOfPlay', models.DO_NOTHING, blank=True, null=True)
    scoring = models.ForeignKey('Scoring', models.DO_NOTHING)
    expected_start = models.DateTimeField(blank=True, null=True)
    actual_start = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=255)
    participants = models.PositiveIntegerField()
    expected_competitiveness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    actual_competitiveness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    expected_eliteness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    actual_eliteness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_competitions')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_competitions')

    def get_absolute_url(self):
        return reverse('athletics.views.competition_details', args=[self.sporting_event.slug, self.slug])

    class Meta:
        db_table = 'competition'
        unique_together = (('sporting_event', 'slug'),)


class CompetitionEvent(models.Model):
    competition = models.OneToOneField(Competition, on_delete=models.DO_NOTHING)
    event = models.ForeignKey('Event', models.DO_NOTHING)
    subevent = models.ForeignKey('Event', models.DO_NOTHING, blank=True, null=True, related_name='created_competition_events')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='last_modified_competition_events')

    class Meta:
        db_table = 'competition_event'


class CompetitionRace(models.Model):
    competition = models.OneToOneField(Competition, on_delete=models.DO_NOTHING)
    timing_system = models.ForeignKey('TimingSystem', models.DO_NOTHING, blank=True, null=True)
    start_interval = models.PositiveIntegerField()
    distance = models.FloatField()
    mode = models.ForeignKey('Mode', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_competition_races')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_competition_races')

    class Meta:
        db_table = 'competition_race'


class CompetitionRaceHurdles(models.Model):
    competition = models.OneToOneField(Competition, on_delete=models.DO_NOTHING)
    height = models.DecimalField(max_digits=4, decimal_places=3)
    unit = models.ForeignKey('utility.Unit', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_competition_race_hurdles')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_competition_race_hurdles')


class CompetitionWeight(models.Model):
    competition = models.OneToOneField(Competition, on_delete=models.DO_NOTHING)
    value = models.DecimalField(max_digits=5, decimal_places=3)
    unit = models.ForeignKey('utility.Unit', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_competition_weight')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_competition_weight')


class CompetitionSimilarity(models.Model):
    competition = models.OneToOneField(Competition, on_delete=models.DO_NOTHING, related_name='similar_competitions')
    other = models.ForeignKey(Competition, models.DO_NOTHING, related_name='other_similar_competitions')
    value = models.DecimalField(max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_competition_similarities')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_competition_similarities')

    class Meta:
        db_table = 'competition_similarity'
        unique_together = (('competition', 'other'),)


class CompetitionType(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_competition_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_competition_types')

    class Meta:
        db_table = 'competition_type'


class Course(models.Model):
    course_type = models.ForeignKey('CourseType', models.DO_NOTHING)
    field_of_play = models.ForeignKey('FieldOfPlay', models.DO_NOTHING)
    surface = models.ForeignKey('Surface', models.DO_NOTHING)
    distance = models.DecimalField(max_digits=12, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_courses')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_courses')

    class Meta:
        db_table = 'course'


class CourseGrade(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    degrees = models.FloatField(blank=True, null=True)
    start = models.DecimalField(max_digits=10, decimal_places=2)
    end = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_course_grades')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_course_grades')

    class Meta:
        db_table = 'course_grade'
        unique_together = (('course', 'sequence'),)


class CourseSimilarity(models.Model):
    course = models.OneToOneField(Course, on_delete=models.DO_NOTHING, related_name='course_similarities')
    other = models.ForeignKey(Course, models.DO_NOTHING, related_name='other_course_similarities')
    value = models.DecimalField(max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_course_similarities')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_course_similarities')

    class Meta:
        db_table = 'course_similarity'
        unique_together = (('course', 'other'),)


class CourseSurface(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    surface = models.ForeignKey('Surface', models.DO_NOTHING)
    start = models.DecimalField(max_digits=10, decimal_places=2)
    end = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_course_surfaces')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_course_surfaces')

    class Meta:
        db_table = 'course_surface'
        unique_together = (('course', 'sequence'),)


class CourseType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_course_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_course_types')

    class Meta:
        db_table = 'course_type'


class Discipline(models.Model):
    sport = models.ForeignKey('Sport', models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_disciplines')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_disciplines')

    class Meta:
        db_table = 'discipline'


class Disqualification(models.Model):
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_disqualifications')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_disqualifications')

    class Meta:
        db_table = 'disqualification'
        unique_together = (('organization', 'code'),)


class Division(models.Model):
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_divisions')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_divisions')

    class Meta:
        db_table = 'division'
        unique_together = (('organization', 'name'),)


class Environment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_environments')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_environments')

    class Meta:
        db_table = 'environment'


class Event(models.Model):
    discipline = models.ForeignKey(Discipline, models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    slug = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_events')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_events')

    class Meta:
        db_table = 'event'


class EventDistance(models.Model):
    event = models.OneToOneField(Event, on_delete=models.DO_NOTHING)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    distance_unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_event_distances')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_event_distances')

    class Meta:
        db_table = 'event_distance'


class EventHurdles(models.Model):
    event = models.OneToOneField(Event, on_delete=models.DO_NOTHING)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    height_unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_event_hurdles')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_event_hurdles')

    class Meta:
        db_table = 'event_hurdles'


class EventWeight(models.Model):
    event = models.OneToOneField(Event, on_delete=models.DO_NOTHING)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    weight_unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_event_weights')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_event_weights')

    class Meta:
        db_table = 'event_weight'


class FieldOfPlay(models.Model):
    id = models.BigAutoField(primary_key=True)
    sport = models.ForeignKey('Sport', models.DO_NOTHING)
    venue = models.ForeignKey('geography.Venue', models.DO_NOTHING, related_name='fields_of_play')
    name = models.CharField(max_length=50)
    established = models.DateTimeField(blank=True, null=True)
    retired = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_fields_of_play')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_fields_of_play')

    class Meta:
        db_table = 'field_of_play'


class Heat(models.Model):
    competition = models.ForeignKey(Competition, models.CASCADE)
    tier = models.ForeignKey('Tier', models.DO_NOTHING)
    is_overall = models.BooleanField()
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_heats')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_heats')

    class Meta:
        db_table = 'heat'


class Legitimacies(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_legitimacies')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_legitimacies', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'legitimacies'
        verbose_name_plural = 'legitimacies'


class SportingEvent(models.Model):
    sporting_event_type = models.ForeignKey('SportingEventType', models.DO_NOTHING)
    environment = models.ForeignKey(Environment, models.DO_NOTHING)
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True)
    division = models.ForeignKey(Division, models.DO_NOTHING, blank=True, null=True)
    venue = models.ForeignKey('geography.Venue', models.DO_NOTHING)
    organizer = models.ForeignKey('identity.Identity', models.DO_NOTHING, null=True, related_name='organized_sporting_events')
    name = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    url = models.CharField(max_length=500)
    championship = models.BooleanField()
    participants = models.PositiveIntegerField()
    expected_competitiveness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    actual_competitiveness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    expected_eliteness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    actual_eliteness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_sporting_events')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_sporting_events', blank=True, null=True)
    categories = models.ManyToManyField(Category, through=CategorySportingEvent)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SportingEvent, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('athletics.views.sportingevent_details', args=[self.sporting_event.slug])

    class Meta:
        db_table = 'sporting_event'


class SportingEventReview(models.Model):
    sporting_event = models.OneToOneField(SportingEvent, on_delete=models.DO_NOTHING)
    review = models.ForeignKey('Review', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_sporting_event_reviews')
    last_modified_at = models.DateTimeField()
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_sporting_event_reviews')

    class Meta:
        db_table = 'sporting_event_review'
        unique_together = (('sporting_event', 'review'),)


class SportingEventType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_sporting_event_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_sporting_event_types', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sporting_event_type'


class Mode(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_modes')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_modes', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mode'


class Outcome(models.Model):
    type = models.ForeignKey('OutcomeType', models.DO_NOTHING, null=True)
    field_of_play = models.ForeignKey(FieldOfPlay, models.DO_NOTHING)
    competition = models.ForeignKey(Competition, models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='performances')
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True, related_name='organization_outcomes')
    place = models.PositiveSmallIntegerField()
    value = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    state = models.ForeignKey('OutcomeState', models.DO_NOTHING)
    legitimacy = models.ForeignKey(Legitimacies, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_outcomes')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_outcomes', blank=True, null=True)

    class Meta:
        db_table = 'outcome'
        unique_together = (('competition', 'identity', ), )


class OutcomeState(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'outcome_state'


class OutcomeType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_outcome_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_outcome_types', blank=True, null=True)

    class Meta:
        db_table = 'outcome_type'


class OutcomeAgeGroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    outcome = models.OneToOneField(Outcome, models.DO_NOTHING)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_performance_age_groups')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_performance_age_groups')

    class Meta:
        db_table = 'outcome_age_group'


class OutcomeAnnotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    outcome = models.ForeignKey(Outcome, models.DO_NOTHING)
    annotation_type = models.ForeignKey(AnnotationType, models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'outcome_annotation'


class OutcomeSimilarity(models.Model):
    outcome = models.OneToOneField(Outcome, on_delete=models.DO_NOTHING)
    other = models.ForeignKey(Outcome, models.DO_NOTHING, related_name='%(class)s_other')
    value = models.DecimalField(max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'outcome_similarity'
        unique_together = (('outcome', 'other'),)


class RaceOutcome(models.Model):
    outcome = models.OneToOneField(Outcome, models.CASCADE)
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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_race_outcomes')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_race_outcomes', blank=True, null=True)

    class Meta:
        db_table = 'race_outcome'


class RaceOutcomeState(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'race_outcome_state'


class RelayOrder(models.Model):
    race_outcome = models.ForeignKey('RaceOutcome', models.CASCADE)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relay_orders')
    sequence = models.SmallIntegerField()
    distance = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'relay_order'
        unique_together = (('race_outcome', 'identity', 'sequence'),)
        verbose_name_plural = 'relay orders'


class RelayMember(models.Model):
    relay = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relay_members')
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relays')
    is_alternate = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        db_table = 'relay_member'
        unique_together = (('relay', 'identity'),)
        verbose_name_plural = 'relay members'


class Review(models.Model):
    user = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    content_language = models.ForeignKey('geography.Language', models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'review'


class ReviewFlag(models.Model):
    user = models.OneToOneField('identity.Identity', on_delete=models.DO_NOTHING)
    review = models.ForeignKey(Review, models.DO_NOTHING)
    flag = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'review_flag'
        unique_together = (('user', 'review'),)


class Rule(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rule'


class Sanctions(models.Model):
    substance = models.ForeignKey('Substances', models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    start_violation_date = models.DateField(blank=True, null=True)
    end_violation_date = models.DateField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'sanctions'
        verbose_name_plural = 'sanctions'


class Scoring(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_scorings')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_scorings')

    class Meta:
        db_table = 'scoring'


class Seed(models.Model):
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    competition = models.ForeignKey(Competition, models.DO_NOTHING)
    seed_method = models.ForeignKey('SeedMethod', models.DO_NOTHING)
    seed_source_id = models.PositiveIntegerField()
    value = models.DecimalField(max_digits=12, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'seed'
        unique_together = (('competition', 'identity', 'seed_method', 'seed_source_id'),)


class SeedMethod(models.Model):
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'seed_method'


class Series(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'series'
        verbose_name_plural = 'series'


class SeriesHierarchy(models.Model):
    parent = models.ForeignKey(Series, on_delete=models.DO_NOTHING, related_name='child_series')
    child = models.ForeignKey(Series, models.DO_NOTHING, related_name='parent_series')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'series_hierarchy'
        unique_together = (('parent', 'child'),)


class SeriesSportingEvent(models.Model):
    series = models.OneToOneField(Series, on_delete=models.DO_NOTHING)
    sporting_event = models.ForeignKey(SportingEvent, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'series_sporting_event'
        unique_together = (('series', 'sporting_event'),)


class SocialClass(models.Model):
    code = models.CharField(unique=True, max_length=8)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'social_class'
        verbose_name = 'social class'
        verbose_name_plural = 'social classes'


class SocialClassAlias(models.Model):
    social_class = models.ForeignKey(SocialClass, models.DO_NOTHING)
    value = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_social_class_aliases')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_social_class_aliases')

    class Meta:
        db_table = 'social_class_alias'
        unique_together = (('social_class', 'value'),)
        verbose_name_plural = 'social class aliases'


class Split(models.Model):
    race_outcome = models.OneToOneField(RaceOutcome, on_delete=models.DO_NOTHING)
    cumulative_distance = models.DecimalField(max_digits=10, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=3)
    cumulative_time = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'split'


class SponsorshipAthlete(models.Model):
    sponsor = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='sponsored_athletes')
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='sponsors')
    amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'sponsorship_athlete'


class SponsorshipCompetition(models.Model):
    sponsor = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    competition = models.ForeignKey(Competition, models.DO_NOTHING)
    amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'sponsorship_competition'


class Sport(models.Model):
    sport_type = models.ForeignKey('SportType', models.DO_NOTHING)
    name = models.CharField(max_length=200)
    description = models.TextField()
    scoring_units = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    wikipedia = models.CharField(max_length=150)
    knowledge_graph = models.OneToOneField('utility.KnowledgeGraph', on_delete=models.DO_NOTHING, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sport'


class SportType(models.Model):
    name = models.CharField(unique=True, max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sport_type'


class Strategy(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'strategy'
        verbose_name_plural = "strategies"


class Substances(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    wikipedia_url = models.CharField(max_length=100)
    is_banned = models.BooleanField()
    banned_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'substances'
        verbose_name_plural = 'substances'


class Surface(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_surfaces')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='last_modified_surfaces')

    class Meta:
        db_table = 'surface'


class Tier(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    level = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tier'


class TimingSystem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'timing_system'
