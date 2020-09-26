from django.contrib import admin
from django import forms
from track_field_project.admin.site import advanced_admin
from sport.models import athletics as models


@admin.register(models.AnnotationAttempt, site=advanced_admin)
class AnnotationAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'sequence', )
    list_select_related = ('attempt', )


@admin.register(models.AnnotationSplit, site=advanced_admin)
class AnnotationSplitAdmin(admin.ModelAdmin):
    list_display = ('race_outcome', 'cumulative_distance', 'distance', 'cumulative_time', 'time')
    list_select_related = ('race_outcome', )


@admin.register(models.Attempt, site=advanced_admin)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('type', 'identity', 'outcome', 'sequence', 'state', 'value', 'wind')
    list_select_related = ('type', 'identity', 'outcome', 'state')


@admin.register(models.AttemptState, site=advanced_admin)
class AttemptStateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(models.Course, site=advanced_admin)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CourseSurface, site=advanced_admin)
class CourseSurfaceAdmin(admin.ModelAdmin):
    list_display = ('course', 'sequence', 'surface')


@admin.register(models.CourseSimilarity, site=advanced_admin)
class CourseSimilarityAdmin(admin.ModelAdmin):
    list_display = ('course', 'other', 'value')
    list_select_related = ('course', 'other')


@admin.register(models.EventDistance, site=advanced_admin)
class EventDistanceAdmin(admin.ModelAdmin):
    list_display = ('event', 'distance', 'distance_unit')
    list_select_related = ('event', 'distance_unit')


@admin.register(models.EventHurdles, site=advanced_admin)
class EventHurdlesAdmin(admin.ModelAdmin):
    list_display = ('event', 'height', 'height_unit')
    list_select_related = ('event', 'height_unit')


@admin.register(models.EventWeight, site=advanced_admin)
class EventWeightAdmin(admin.ModelAdmin):
    list_display = ('event', 'weight', 'weight_unit')
    list_select_related = ('event', 'weight_unit')


@admin.register(models.Heat, site=advanced_admin)
class HeatAdmin(admin.ModelAdmin):
    list_display = ('competition', 'tier', 'is_overall', 'name')
    list_select_related = ('competition', 'tier')


@admin.register(models.RaceOutcome, site=advanced_admin)
class RaceOutcomeAdmin(admin.ModelAdmin):
    list_display = ('outcome', 'heat', 'mode', 'state')
    list_select_related = ('outcome', 'heat', 'mode', 'state')


@admin.register(models.RaceOutcomeState, site=advanced_admin)
class RaceOutcomeStateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(models.RelayOrder, site=advanced_admin)
class RelayOrderAdmin(admin.ModelAdmin):
    list_display = ('race_outcome', 'identity', 'sequence', 'distance')


@admin.register(models.Seed, site=advanced_admin)
class SeedAdmin(admin.ModelAdmin):
    list_display = ('competition', 'identity', 'seed_method')


@admin.register(models.SeedMethod, site=advanced_admin)
class SeedMethodAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Split, site=advanced_admin)
class SplitAdmin(admin.ModelAdmin):
    list_display = ('race_outcome', 'cumulative_distance', 'distance', 'cumulative_time', 'time')


@admin.register(models.TimingSystem, site=advanced_admin)
class TimingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', )
