from django.db import models

# Create your models here.

class Annotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    annotation_type = models.ForeignKey('AnnotationType', models.DO_NOTHING)
    is_public = models.BooleanField()
    is_verified = models.BooleanField()
    verified_by = models.PositiveIntegerField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_annotations')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_annotations')
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'annotation'


class AnnotationAttempt(models.Model):
    attempt = models.ForeignKey('Attempt', models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_annotation_attempts')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_annotation_attempts')
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'annotation_attempt'


class AnnotationSplit(models.Model):
    performance = models.ForeignKey('Performance', models.DO_NOTHING)
    cumulative_distance = models.DecimalField(max_digits=10, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=3)
    cumulative_time = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_annotation_splits')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_annotation_splits')
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'annotation_split'


class AnnotationType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_annotation_types')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_annotation_types')

    class Meta:
        db_table = 'annotation_type'


class AnnotationVote(models.Model):
    id = models.BigAutoField(primary_key=True)
    annotation = models.ForeignKey(Annotation, models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    up = models.BooleanField()
    down = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_annotation_votes')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_annotation_votes')

    class Meta:
        db_table = 'annotation_vote'
        unique_together = (('annotation', 'identity', 'up', 'down'),)


class Attempt(models.Model):
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    heat = models.ForeignKey('Heat', models.DO_NOTHING)
    performance = models.ForeignKey('Performance', models.DO_NOTHING)
    state = models.ForeignKey('PerformanceState', models.DO_NOTHING)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    wind = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_attempts')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_attempts')
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'attempt'


class AttemptSequential(models.Model):
    attempt = models.OneToOneField(Attempt, on_delete=models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'attempt_sequential'
        unique_together = (('attempt', 'sequence'),)


class AttemptThreshold(models.Model):
    attempt = models.ForeignKey(Attempt, models.DO_NOTHING, primary_key=True)
    sequence = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'attempt_threshold'
        unique_together = (('attempt', 'sequence'),)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=255)

    class Meta:
        db_table = 'category'


class CategoryHierarchy(models.Model):
    parent = models.ForeignKey(Category, models.DO_NOTHING, related_name='parent_category')
    child = models.ForeignKey(Category, models.DO_NOTHING, related_name='child_category')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'category_hierarchy'
        unique_together = (('parent', 'child'),)


class CategoryMeet(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING)
    meet = models.OneToOneField('Meet', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'category_meet'
        unique_together = (('meet', 'category'),)


class Coach(models.Model):
    coach = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    athlete = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='coaches')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'coach'


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    reply_to_comment = models.ForeignKey('self', models.DO_NOTHING, null=True)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    is_flagged = models.PositiveIntegerField()
    flagged_by = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'comment'


class Competition(models.Model):
    meet_instance = models.ForeignKey('MeetInstance', models.DO_NOTHING)
    division = models.ForeignKey('Division', models.DO_NOTHING)
    event = models.ForeignKey('Event', models.DO_NOTHING)
    subevent = models.ForeignKey('Event', models.DO_NOTHING, related_name='multi_events', blank=True, null=True)
    mode = models.ForeignKey('Mode', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('Course', models.DO_NOTHING, blank=True, null=True)
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
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'competition'


class CompetitionSimilarity(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)
    other = models.ForeignKey(Competition, models.DO_NOTHING, related_name='%(class)s_other')
    value = models.DecimalField(max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'competition_similarity'
        unique_together = (('competition', 'other'),)


class Course(models.Model):
    venue = models.ForeignKey('geography.Venue', models.DO_NOTHING)
    terrain = models.ForeignKey('geography.Terrain', models.DO_NOTHING)
    name = models.CharField(max_length=50)
    distance = models.DecimalField(max_digits=12, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'course'


class CourseSegment(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    terrain = models.ForeignKey('geography.Terrain', models.DO_NOTHING, blank=True, null=True)
    grade = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    start = models.DecimalField(max_digits=10, decimal_places=2)
    end = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    class Meta:
        db_table = 'course_segment'
        unique_together = (('course', 'sequence'),)


class CourseSimilarity(models.Model):
    course = models.OneToOneField(Course, on_delete=models.DO_NOTHING)
    other = models.ForeignKey('geography.Country', models.DO_NOTHING, related_name='%(class)s_other')
    value = models.DecimalField(max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'course_similarity'
        unique_together = (('course', 'other'),)


class Discipline(models.Model):
    sport = models.ForeignKey('Sport', models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'discipline'


class Disqualification(models.Model):
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'disqualification'
        unique_together = (('organization', 'code'),)


class Division(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'division'


class Environment(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'environment'


class Event(models.Model):
    discipline = models.ForeignKey(Discipline, models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50)
    slug = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'event'


class EventDistance(models.Model):
    event = models.OneToOneField(Event, on_delete=models.DO_NOTHING, primary_key=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    distance_unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_event_distances')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_event_distances')

    class Meta:
        db_table = 'event_distance'


class EventHurdles(models.Model):
    event = models.OneToOneField(Event, on_delete=models.DO_NOTHING, primary_key=True)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    height_unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'event_hurdles'


class EventWeight(models.Model):
    event = models.OneToOneField(Event, on_delete=models.DO_NOTHING, primary_key=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    weight_unit = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'event_weight'


class Heat(models.Model):
    competition = models.ForeignKey(Competition, models.DO_NOTHING)
    tier = models.ForeignKey('Tier', models.DO_NOTHING)
    overall = models.IntegerField()
    name = models.CharField(max_length=75)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    class Meta:
        db_table = 'heat'
        unique_together = (('competition', 'tier', 'name'),)


class HeatClustering(models.Model):
    heat = models.ForeignKey(Heat, models.DO_NOTHING)
    split_distance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id = models.PositiveIntegerField(primary_key=True)
    min_eps = models.DecimalField(max_digits=10, decimal_places=3)
    max_eps = models.DecimalField(max_digits=10, decimal_places=3)
    min_points = models.PositiveIntegerField()
    max_points = models.PositiveIntegerField()
    fuzzy = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'heat_clustering'
        unique_together = (('heat', 'id', 'min_eps', 'min_points', 'max_eps', 'max_points', 'fuzzy'),)


class HeatClusteringAssignments(models.Model):
    clustering = models.ForeignKey(HeatClustering, models.DO_NOTHING)
    performance = models.ForeignKey('Performance', models.DO_NOTHING)
    split = models.ForeignKey('Split', models.DO_NOTHING, blank=True, null=True)
    cluster = models.IntegerField()
    membership = models.DecimalField(max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'heat_clustering_assignments'
        unique_together = (('clustering', 'performance', 'cluster'),)


class HeatSimilarity(models.Model):
    heat = models.OneToOneField(Heat, on_delete=models.DO_NOTHING)
    other = models.ForeignKey(Heat, models.DO_NOTHING, related_name='%(class)s_other')
    value = models.DecimalField(max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'heat_similarity'
        unique_together = (('heat', 'other'),)


class Legitimacies(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'legitimacies'


class Meet(models.Model):
    meet_type = models.ForeignKey('MeetType', models.DO_NOTHING)
    environment = models.ForeignKey(Environment, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=255)
    championship = models.IntegerField()
    participants = models.PositiveIntegerField()
    expected_competitiveness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    actual_competitiveness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    expected_eliteness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    actual_eliteness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    class Meta:
        db_table = 'meet'


class MeetInstance(models.Model):
    timing_system = models.ForeignKey('TimingSystem', models.DO_NOTHING, blank=True, null=True)
    meet = models.ForeignKey(Meet, models.DO_NOTHING)
    venue = models.ForeignKey('geography.Venue', models.DO_NOTHING)
    name = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    url = models.CharField(max_length=500)
    participants = models.PositiveIntegerField()
    expected_competitiveness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    actual_competitiveness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    expected_eliteness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    actual_eliteness = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'meet_instance'


class MeetInstanceReview(models.Model):
    meet_instance = models.OneToOneField(MeetInstance, on_delete=models.DO_NOTHING)
    review = models.ForeignKey('Review', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField()
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by')

    class Meta:
        db_table = 'meet_instance_review'
        unique_together = (('meet_instance', 'review'),)


class MeetType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'meet_type'


class Mode(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    class Meta:
        db_table = 'mode'


class OrganizationMembership(models.Model):
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='members')
    member = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='%(class)s')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'organization_membership'
        unique_together = (('organization', 'member'),)


class Performance(models.Model):
    heat = models.ForeignKey(Heat, models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='performances')
    organization = models.ForeignKey('identity.Identity', models.DO_NOTHING, blank=True, null=True)
    social_class = models.ForeignKey('SocialClass', models.DO_NOTHING, blank=True, null=True)
    squad = models.CharField(max_length=1, blank=True, null=True)
    place = models.PositiveSmallIntegerField()
    points = models.SmallIntegerField()
    value = models.DecimalField(max_digits=12, decimal_places=4)
    reaction_time = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    wind = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    unattached = models.IntegerField(blank=True, null=True)
    state = models.ForeignKey('PerformanceState', models.DO_NOTHING)
    strategy = models.ForeignKey('Strategy', models.DO_NOTHING, blank=True, null=True)
    legitimacy = models.ForeignKey(Legitimacies, models.DO_NOTHING)
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'performance'
        unique_together = (('heat', 'organization', 'identity', 'squad', 'value', 'state'),)


class PerformanceAnnotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    performance = models.ForeignKey(Performance, models.DO_NOTHING)
    annotation_type = models.ForeignKey(AnnotationType, models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'performance_annotation'


class PerformanceSimilarity(models.Model):
    performance = models.OneToOneField(Performance, on_delete=models.DO_NOTHING)
    other = models.ForeignKey(Performance, models.DO_NOTHING, related_name='%(class)s_other')
    value = models.DecimalField(max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'performance_similarity'
        unique_together = (('performance', 'other'),)


class PerformanceState(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'performance_state'


class RelayMembers(models.Model):
    relay = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relay_members')
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relays')
    is_alternate = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'relay_members'
        unique_together = (('relay', 'identity'),)


class RelayPerformanceParticipants(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    relay = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relay_participants_relays')
    member = models.ForeignKey('identity.Identity', models.DO_NOTHING, related_name='relay_participants')
    performance = models.ForeignKey(Performance, models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_relay_participants')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_relay_participants')

    class Meta:
        db_table = 'relay_performance_participants'
        unique_together = (('performance', 'relay', 'member'),)


class RelaySplit(models.Model):
    performance = models.ForeignKey(Performance, models.DO_NOTHING)
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    leg = models.PositiveIntegerField()
    cumulative_distance = models.DecimalField(max_digits=10, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=3)
    leg_distance = models.DecimalField(max_digits=10, decimal_places=3)
    cumulative_time = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.DecimalField(max_digits=10, decimal_places=3)
    leg_time = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'relay_split'
        unique_together = (('performance', 'identity'),)


class Review(models.Model):
    user = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    content_language = models.ForeignKey('geography.Language', models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'review'


class ReviewFlag(models.Model):
    user = models.OneToOneField('identity.Identity', on_delete=models.DO_NOTHING)
    review = models.ForeignKey(Review, models.DO_NOTHING)
    flag = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
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
    last_updated = models.DateTimeField(blank=True, null=True)
    last_updated_by = models.PositiveIntegerField(blank=True, null=True)

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
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'sanctions'


class Seed(models.Model):
    identity = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    competition = models.ForeignKey(Competition, models.DO_NOTHING)
    seed_method = models.ForeignKey('SeedMethod', models.DO_NOTHING)
    seed_source_id = models.PositiveIntegerField()
    value = models.DecimalField(max_digits=12, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'seed'
        unique_together = (('competition', 'identity', 'seed_method', 'seed_source_id'),)


class SeedMethod(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'seed_method'


class Series(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'series'


class SeriesHierarchy(models.Model):
    parent = models.OneToOneField(Series, on_delete=models.DO_NOTHING, related_name='child_series')
    child = models.ForeignKey(Series, models.DO_NOTHING, related_name='parent_series')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'series_hierarchy'
        unique_together = (('parent', 'child'),)


class SeriesMeet(models.Model):
    series = models.OneToOneField(Series, on_delete=models.DO_NOTHING)
    meet = models.ForeignKey(Meet, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'series_meet'
        unique_together = (('series', 'meet'),)


class SocialClass(models.Model):
    code = models.CharField(unique=True, max_length=8)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'social_class'


class SocialClassAlias(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    social_class = models.ForeignKey(SocialClass, models.DO_NOTHING)
    value = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_social_class_aliases')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_social_class_aliases')

    class Meta:
        db_table = 'social_class_alias'
        unique_together = (('social_class', 'value'),)


class Split(models.Model):
    performance = models.OneToOneField(Performance, on_delete=models.DO_NOTHING)
    cumulative_distance = models.DecimalField(max_digits=10, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=3)
    cumulative_time = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

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
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'sponsorship_athlete'


class SponsorshipCompetition(models.Model):
    sponsor = models.ForeignKey('identity.Identity', models.DO_NOTHING)
    competition = models.ForeignKey(Competition, models.DO_NOTHING)
    amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'sponsorship_competition'


class Sport(models.Model):
    sport_type = models.ForeignKey('SportType', models.DO_NOTHING)
    name = models.CharField(max_length=200)
    description = models.TextField()
    scoring_units = models.ForeignKey('utility.Unit', models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    wikipedia = models.CharField(max_length=150)
    knowledge_graph = models.OneToOneField('utility.KnowledgeGraph', on_delete=models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'sport'


class SportType(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'sport_type'


class StagingAttempt(models.Model):
    identity = models.ForeignKey('identity.StagingIdentity', models.DO_NOTHING)
    heat_id = models.PositiveIntegerField()
    performance = models.ForeignKey('StagingPerformance', models.DO_NOTHING)
    state = models.ForeignKey(PerformanceState, models.DO_NOTHING)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    wind = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'staging_attempt'


class StagingAttemptSequential(models.Model):
    attempt = models.OneToOneField(StagingAttempt, on_delete=models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'staging_attempt_sequential'
        unique_together = (('attempt', 'sequence'),)


class StagingAttemptThreshold(models.Model):
    attempt = models.OneToOneField(StagingAttempt, on_delete=models.DO_NOTHING)
    sequence = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'staging_attempt_threshold'
        unique_together = (('attempt', 'sequence'),)


class StagingCompetition(models.Model):
    staging_meet_instance = models.ForeignKey('StagingMeetInstance', models.DO_NOTHING)
    staging_division = models.ForeignKey(Division, models.DO_NOTHING)
    event = models.ForeignKey(Event, models.DO_NOTHING, related_name='staging_competition',)
    subevent = models.ForeignKey(Event, models.DO_NOTHING, related_name='staging_subcompetition', blank=True, null=True)
    mode = models.ForeignKey(Mode, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    url = models.CharField(max_length=255)
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'staging_competition'


class StagingEntity(models.Model):
    entity_type = models.ForeignKey('identity.EntityType', models.DO_NOTHING)
    name = models.CharField(max_length=150)
    knowledge_graph = models.ForeignKey('utility.KnowledgeGraph', models.DO_NOTHING)
    website = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'staging_entity'


class StagingHeat(models.Model):
    staging_competition = models.ForeignKey(Competition, models.DO_NOTHING)
    staging_tier = models.ForeignKey('Tier', models.DO_NOTHING)
    overall = models.IntegerField()
    name = models.CharField(max_length=75)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    class Meta:
        db_table = 'staging_heat'
        unique_together = (('staging_competition', 'staging_tier', 'name'),)


class StagingMeet(models.Model):
    meet_type = models.ForeignKey(MeetType, models.DO_NOTHING)
    environment = models.ForeignKey(Environment, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    championship = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    class Meta:
        db_table = 'staging_meet'


class StagingMeetInstance(models.Model):
    timing_system_id = models.PositiveIntegerField(blank=True, null=True)
    staging_meet = models.ForeignKey(StagingMeet, models.DO_NOTHING)
    staging_venue = models.ForeignKey('StagingVenue', models.DO_NOTHING)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    url = models.CharField(max_length=500)
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'staging_meet_instance'


class StagingPerformance(models.Model):
    staging_heat = models.ForeignKey(StagingHeat, models.DO_NOTHING)
    staging_identity_id = models.PositiveIntegerField()
    staging_organization_id = models.PositiveIntegerField(blank=True, null=True)
    social_class = models.ForeignKey(SocialClass, models.DO_NOTHING, blank=True, null=True)
    squad = models.CharField(max_length=1, blank=True, null=True)
    place = models.PositiveSmallIntegerField()
    points = models.SmallIntegerField()
    value = models.DecimalField(max_digits=12, decimal_places=4)
    reaction_time = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    wind = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    unattached = models.IntegerField(blank=True, null=True)
    state = models.ForeignKey(PerformanceState, models.DO_NOTHING)
    strategy = models.ForeignKey('Strategy', models.DO_NOTHING, blank=True, null=True)
    legitimacy = models.ForeignKey(Legitimacies, models.DO_NOTHING)
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'staging_performance'
        unique_together = (('staging_heat', 'staging_organization_id', 'staging_identity_id', 'squad', 'value', 'state'),)


class StagingRelayMembers(models.Model):
    staging_relay = models.ForeignKey('identity.StagingIdentity', models.DO_NOTHING, related_name='%(class)s_relay')
    staging_identity = models.ForeignKey('identity.StagingIdentity', models.DO_NOTHING, related_name='%(class)s_identity')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'staging_relay_members'
        unique_together = (('staging_relay', 'staging_identity'),)


class StagingRelayPerformanceParticipants(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    relay = models.ForeignKey('identity.StagingIdentity', models.DO_NOTHING, related_name='staging_relay_participants_relays')
    member = models.ForeignKey('identity.StagingIdentity', models.DO_NOTHING, related_name='staging_relay_participants_members')
    performance = models.ForeignKey(Performance, models.DO_NOTHING)
    sequence = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_staging_relay_participants')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', blank=True, null=True, related_name='modified_staging_relay_participants')

    class Meta:
        db_table = 'staging_relay_performance_participants'
        unique_together = (('performance', 'relay', 'member'),)


class StagingRelaySplit(models.Model):
    staging_performance = models.ForeignKey(StagingPerformance, models.DO_NOTHING)
    staging_identity = models.ForeignKey('identity.StagingIdentity', models.DO_NOTHING)
    leg = models.PositiveIntegerField()
    cumulative_distance = models.DecimalField(max_digits=10, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=3)
    leg_distance = models.DecimalField(max_digits=10, decimal_places=3)
    cumulative_time = models.DecimalField(max_digits=10, decimal_places=3)
    time = models.DecimalField(max_digits=10, decimal_places=3)
    leg_time = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'staging_relay_split'
        unique_together = (('staging_performance', 'staging_identity'),)


class StagingVenue(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    elevation = models.DecimalField(max_digits=12, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    class Meta:
        db_table = 'staging_venue'


class Strategy(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=20)

    class Meta:
        db_table = 'strategy'


class Substances(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    wikipedia_url = models.CharField(max_length=100)
    is_banned = models.PositiveIntegerField()
    banned_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'substances'


class Tier(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255)
    level = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'tier'


class TimingSystem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)
    source = models.CharField(max_length=25)

    class Meta:
        db_table = 'timing_system'
