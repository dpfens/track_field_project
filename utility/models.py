from django.db import models

# Create your models here.
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
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'knowledge_graph'


class Language(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    iso_639_3 = models.CharField(max_length=3, blank=True, null=True)
    iso_639_2 = models.CharField(max_length=11, blank=True, null=True)
    iso_639_1 = models.CharField(max_length=2, blank=True, null=True)
    name = models.CharField(max_length=58, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'language'


class LanguageVariant(models.Model):
    language = models.ForeignKey(Language, models.DO_NOTHING)
    iso_639_1 = models.CharField(max_length=14, blank=True, null=True)
    language_code = models.CharField(max_length=4, blank=True, null=True)
    territory = models.CharField(max_length=3, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'language_variant'


class Quantity(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)
    description = models.TextField()
    wikipedia_url = models.CharField(max_length=150)
    symbol = models.CharField(max_length=10)
    si_unit = models.ForeignKey('Unit', models.DO_NOTHING, related_name='si_quantity')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        managed = False
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
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unit'
        unique_together = (('unit_system', 'quantity', 'name'),)


class UnitSystem(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)
    description = models.TextField()
    wikipedia_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unit_system'
