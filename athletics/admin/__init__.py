from django.contrib import admin
from django import forms
from track_field_project.admin.site import advanced_admin
from athletics import models


@admin.register(models.Annotation, site=advanced_admin)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('annotation_type', 'is_verified', 'is_public')
    list_select_related = ('annotation_type', )


@admin.register(models.AnnotationAttempt, site=advanced_admin)
class AnnotationAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'sequence', )
    list_select_related = ('attempt', )


@admin.register(models.AnnotationSplit, site=advanced_admin)
class AnnotationSplitAdmin(admin.ModelAdmin):
    list_display = ('race_outcome', 'cumulative_distance', 'distance', 'cumulative_time', 'time')
    list_select_related = ('race_outcome', )


@admin.register(models.AnnotationType, site=advanced_admin)
class AnnotationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.AnnotationVote, site=advanced_admin)
class AnnotationVoteAdmin(admin.ModelAdmin):
    list_display = ('annotation', 'up', 'down')


@admin.register(models.Attempt, site=advanced_admin)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('type', 'identity', 'outcome', 'sequence', 'state', 'value', 'wind')
    list_select_related = ('type', 'identity', 'outcome', 'state')


@admin.register(models.AttemptState, site=advanced_admin)
class AttemptStateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(models.Category, site=advanced_admin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.CategoryHierarchy, site=advanced_admin)
class CategoryHierarchyAdmin(admin.ModelAdmin):
    list_display = ('parent', 'child')
    list_select_related = ('parent', 'child')


@admin.register(models.Coach, site=advanced_admin)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('coach', 'athlete')


@admin.register(models.Comment, site=advanced_admin)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('reply_to_comment', 'identity', 'subject', 'is_flagged')
    list_select_related = ('reply_to_comment', 'identity')


@admin.register(models.Competition, site=advanced_admin)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('division', 'sporting_event')
    list_select_related = ('division', 'sporting_event')


@admin.register(models.CompetitionSimilarity, site=advanced_admin)
class CompetitionSimilarityAdmin(admin.ModelAdmin):
    list_display = ('competition', 'other', 'value')


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


@admin.register(models.Discipline, site=advanced_admin)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('sport', 'name')
    list_select_related = ('sport', )


@admin.register(models.Disqualification, site=advanced_admin)
class DisqualificationAdmin(admin.ModelAdmin):
    list_display = ('organization', 'code', 'name')


@admin.register(models.Division, site=advanced_admin)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Environment, site=advanced_admin)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Event, site=advanced_admin)
class EventAdmin(admin.ModelAdmin):
    list_display = ('discipline', 'name', )
    list_select_related = ('discipline', )


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


@admin.register(models.FieldOfPlay, site=advanced_admin)
class FieldOfPlayAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue')


@admin.register(models.Heat, site=advanced_admin)
class HeatAdmin(admin.ModelAdmin):
    list_display = ('competition', 'tier', 'is_overall', 'name')
    list_select_related = ('competition', 'tier')


@admin.register(models.Legitimacies, site=advanced_admin)
class LegitimaciesAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.SportingEvent, site=advanced_admin)
class SportingEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'sporting_event_type', 'environment', 'championship')
    list_select_related = ('sporting_event_type', 'environment')


@admin.register(models.SportingEventReview, site=advanced_admin)
class SportingEventReviewAdmin(admin.ModelAdmin):
    list_display = ('sporting_event', 'review')

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("start_date (%s) must be before end_date (%s)" % (self.start_date, self.end_date))
        return self.cleaned_data


@admin.register(models.SportingEventType, site=advanced_admin)
class SportingEventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Mode, site=advanced_admin)
class ModeAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Outcome, site=advanced_admin)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('identity', 'organization', 'place', 'value', 'legitimacy')
    list_select_related = ('identity', 'organization')


@admin.register(models.OutcomeAnnotation, site=advanced_admin)
class OutcomeAnnotationAdmin(admin.ModelAdmin):
    list_display = ('user', 'annotation_type', 'outcome')
    list_select_related = ('user', 'annotation_type', 'outcome')


@admin.register(models.OutcomeSimilarity, site=advanced_admin)
class OutcomeSimilarityAdmin(admin.ModelAdmin):
    list_display = ('outcome', 'other', 'value')


@admin.register(models.OutcomeState, site=advanced_admin)
class OutcomeStateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


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


@admin.register(models.Review, site=advanced_admin)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'content_language')


@admin.register(models.ReviewFlag, site=advanced_admin)
class ReviewFlagAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'flag')


@admin.register(models.Rule, site=advanced_admin)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('organization', 'code', 'name')


@admin.register(models.Sanctions, site=advanced_admin)
class SanctionAdmin(admin.ModelAdmin):
    list_display = ('substance', 'identity', 'start_violation_date', 'end_violation_date')


@admin.register(models.Seed, site=advanced_admin)
class SeedAdmin(admin.ModelAdmin):
    list_display = ('competition', 'identity', 'seed_method')


@admin.register(models.SeedMethod, site=advanced_admin)
class SeedMethodAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Series, site=advanced_admin)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.SeriesHierarchy, site=advanced_admin)
class SeriesHierarchyAdmin(admin.ModelAdmin):
    list_display = ('parent', 'child')


@admin.register(models.SeriesSportingEvent, site=advanced_admin)
class SeriesSportingEventAdmin(admin.ModelAdmin):
    list_display = ('sporting_event', 'series')


@admin.register(models.SocialClass, site=advanced_admin)
class SocialClassAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )


@admin.register(models.SocialClassAlias, site=advanced_admin)
class SocialClassAliasAdmin(admin.ModelAdmin):
    list_display = ('value', 'social_class', )


@admin.register(models.Split, site=advanced_admin)
class SplitAdmin(admin.ModelAdmin):
    list_display = ('race_outcome', 'cumulative_distance', 'distance', 'cumulative_time', 'time')


@admin.register(models.SponsorshipAthlete, site=advanced_admin)
class SponsorshipAthleteAdmin(admin.ModelAdmin):
    list_display = ('identity', 'sponsor', 'amount', 'start_date', 'end_date')


@admin.register(models.SponsorshipCompetition, site=advanced_admin)
class SponsorshipCompetitionAdmin(admin.ModelAdmin):
    list_display = ('competition', 'sponsor', 'amount', 'start_date', 'end_date')


@admin.register(models.Sport, site=advanced_admin)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport_type', 'scoring_units')
    list_select_related = ('sport_type', 'scoring_units')


@admin.register(models.SportType, site=advanced_admin)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Strategy, site=advanced_admin)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Substances, site=advanced_admin)
class SubstancesAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_banned')

    class Meta:
        verbose_name_plural = 'substances'


@admin.register(models.Tier, site=advanced_admin)
class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')


@admin.register(models.TimingSystem, site=advanced_admin)
class TimingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', )
