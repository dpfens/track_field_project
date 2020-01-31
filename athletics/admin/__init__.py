from django.contrib import admin
from track_field_project.admin.site import advanced_admin
from athletics import models

@admin.register(models.Annotation, site=advanced_admin)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('annotation_type', 'is_verified', 'is_public')

@admin.register(models.AnnotationAttempt, site=advanced_admin)
class AnnotationAttemptAdmin(admin.ModelAdmin):
    list_display = ('sequence', )

@admin.register(models.AnnotationSplit, site=advanced_admin)
class AnnotationSplitAdmin(admin.ModelAdmin):
    list_display = ('cumulative_distance', 'distance', 'cumulative_time', 'time')

@admin.register(models.AnnotationType, site=advanced_admin)
class AnnotationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.AnnotationVote, site=advanced_admin)
class AnnotationVoteAdmin(admin.ModelAdmin):
    list_display = ('annotation', 'up', 'down')

@admin.register(models.Attempt, site=advanced_admin)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('identity', 'heat', 'performance', 'state', 'value', 'wind')

@admin.register(models.Category, site=advanced_admin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.CategoryHierarchy, site=advanced_admin)
class CategoryHierarchyAdmin(admin.ModelAdmin):
    list_display = ('parent', 'child')

@admin.register(models.CategoryMeet, site=advanced_admin)
class CategoryMeetAdmin(admin.ModelAdmin):
    list_display = ('category', 'meet')

@admin.register(models.Coach, site=advanced_admin)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('coach', 'athlete')

@admin.register(models.Comment, site=advanced_admin)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('reply_to_comment', 'identity', 'subject', 'is_flagged')

@admin.register(models.Competition, site=advanced_admin)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('meet_instance', 'division', 'event', 'subevent', 'mode', 'course')

@admin.register(models.CompetitionSimilarity, site=advanced_admin)
class CompetitionSimilarityAdmin(admin.ModelAdmin):
    list_display = ('competition', 'other', 'value')

@admin.register(models.Course, site=advanced_admin)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('venue', 'terrain')

@admin.register(models.CourseSegment, site=advanced_admin)
class CourseSegmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'sequence', 'terrain', 'grade')

@admin.register(models.CourseSimilarity, site=advanced_admin)
class CourseSimilarityAdmin(admin.ModelAdmin):
    list_display = ('course', 'other', 'value')

@admin.register(models.Discipline, site=advanced_admin)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('sport', 'name')

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

@admin.register(models.EventDistance, site=advanced_admin)
class EventDistanceAdmin(admin.ModelAdmin):
    list_display = ('event', 'distance', 'distance_unit')

@admin.register(models.EventHurdles, site=advanced_admin)
class EventHurdlesAdmin(admin.ModelAdmin):
    list_display = ('event', 'height', 'height_unit')

@admin.register(models.EventWeight, site=advanced_admin)
class EventWeightAdmin(admin.ModelAdmin):
    list_display = ('event', 'weight', 'weight_unit')

@admin.register(models.Heat, site=advanced_admin)
class HeatAdmin(admin.ModelAdmin):
    list_display = ('name', 'competition', 'tier', 'overall')

@admin.register(models.HeatClustering, site=advanced_admin)
class HeatClusteringAdmin(admin.ModelAdmin):
    list_display = ('heat', 'fuzzy', 'min_eps', 'max_eps', 'min_points', 'max_points', 'split_distance')

@admin.register(models.HeatClusteringAssignments, site=advanced_admin)
class HeatClusteringAssignmentsgAdmin(admin.ModelAdmin):
    list_display = ('clustering', 'performance', 'split', 'cluster', 'membership')

@admin.register(models.HeatSimilarity, site=advanced_admin)
class HeatSimilarityAdmin(admin.ModelAdmin):
    list_display = ('heat', 'other', 'value')

@admin.register(models.Legitimacies, site=advanced_admin)
class LegitimaciesAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.Meet, site=advanced_admin)
class MeetAdmin(admin.ModelAdmin):
    list_display = ('name', 'meet_type', 'environment', 'championship')

@admin.register(models.MeetInstance, site=advanced_admin)
class MeetInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'timing_system', 'meet', 'venue')

@admin.register(models.MeetInstanceReview, site=advanced_admin)
class MeetInstanceReviewAdmin(admin.ModelAdmin):
    list_display = ('meet_instance', 'review')

@admin.register(models.MeetType, site=advanced_admin)
class MeetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.Mode, site=advanced_admin)
class ModeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.OrganizationMembership, site=advanced_admin)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ('organization', 'member', 'start_date', 'end_date')

@admin.register(models.Performance, site=advanced_admin)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('heat', 'identity', 'organization', 'social_class', 'place', 'value', 'state', 'legitimacy')

@admin.register(models.PerformanceAnnotation, site=advanced_admin)
class PerformanceAnnotationAdmin(admin.ModelAdmin):
    list_display = ('user', 'annotation_type', 'performance')

@admin.register(models.PerformanceSimilarity, site=advanced_admin)
class PerformanceSimilarityAdmin(admin.ModelAdmin):
    list_display = ('performance', 'other', 'value')

@admin.register(models.PerformanceState, site=advanced_admin)
class PerformanceStateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(models.RelayMembers, site=advanced_admin)
class RelayMembersAdmin(admin.ModelAdmin):
    list_display = ('relay', 'identity', 'is_alternate')

@admin.register(models.RelaySplit, site=advanced_admin)
class RelaySplitAdmin(admin.ModelAdmin):
    list_display = ('performance', 'identity', 'leg', 'cumulative_distance', 'distance', 'leg_distance', 'cumulative_time', 'time', 'leg_time')

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

@admin.register(models.SeriesMeet, site=advanced_admin)
class SeriesMeetAdmin(admin.ModelAdmin):
    list_display = ('meet', 'series')

@admin.register(models.SocialClass, site=advanced_admin)
class SocialClassAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )

@admin.register(models.SocialClassAlias, site=advanced_admin)
class SocialClassAliasAdmin(admin.ModelAdmin):
    list_display = ('value', 'social_class', )

@admin.register(models.Split, site=advanced_admin)
class SplitAdmin(admin.ModelAdmin):
    list_display = ('performance', 'cumulative_distance', 'distance', 'cumulative_time', 'time')

@admin.register(models.SponsorshipAthlete, site=advanced_admin)
class SponsorshipAthleteAdmin(admin.ModelAdmin):
    list_display = ('identity', 'sponsor', 'amount', 'start_date', 'end_date')

@admin.register(models.SponsorshipCompetition, site=advanced_admin)
class SponsorshipCompetitionAdmin(admin.ModelAdmin):
    list_display = ('competition', 'sponsor', 'amount', 'start_date', 'end_date')

@admin.register(models.Sport, site=advanced_admin)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport_type', 'scoring_units')

@admin.register(models.SportType, site=advanced_admin)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.Strategy, site=advanced_admin)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.Substances, site=advanced_admin)
class SubstancesAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_banned')

@admin.register(models.Tier, site=advanced_admin)
class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')

@admin.register(models.TimingSystem, site=advanced_admin)
class TimingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', )
