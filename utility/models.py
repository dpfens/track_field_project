from django.db import models


# Create your models here.
class Feedback(models.Model):
    identity = models.ForeignKey('identity.Identity', on_delete=models.DO_NOTHING, null=True)
    url = models.CharField(max_length=250)
    feedback_type = models.ForeignKey('FeedbackType', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(blank=True, null=True, auto_now=True)


class FeedbackType(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='created_feedback_types')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='last_modified_feedback_types', blank=True, null=True)


class KnowledgeGraph(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    image_content_url = models.CharField(max_length=250, blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    article_body = models.CharField(max_length=2000)
    wikipedia = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        db_table = 'knowledge_graph'


class Quantity(models.Model):
    name = models.CharField(unique=True, max_length=150)
    description = models.TextField()
    wikipedia_url = models.CharField(max_length=150)
    symbol = models.CharField(max_length=10)
    si_unit = models.ForeignKey('Unit', models.DO_NOTHING, null=True, related_name='si_quantity')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'quantity'

class Unit(models.Model):
    unit_system = models.ForeignKey('UnitSystem', models.DO_NOTHING)
    quantity = models.ForeignKey(Quantity, models.DO_NOTHING)
    name = models.CharField(max_length=150)
    description = models.TextField()
    acronym = models.CharField(max_length=5)
    abbreviation = models.CharField(max_length=10)
    wikipedia_url = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'unit'
        unique_together = (('unit_system', 'quantity', 'name'),)


class UnitSystem(models.Model):
    name = models.CharField(unique=True, max_length=150)
    description = models.TextField()
    wikipedia_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'unit_system'
