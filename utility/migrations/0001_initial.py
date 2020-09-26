# Generated by Django 3.1.4 on 2021-01-04 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('dimension', models.CharField(choices=[('E', 'Event'), ('F', 'Event Instance'), ('I', 'Identity'), ('C', 'Competition'), ('H', 'Heat'), ('O', 'Outcome'), ('S', 'Split')], max_length=25)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeedbackType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('description', models.TextField()),
                ('wikipedia_url', models.CharField(max_length=150)),
                ('symbol', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trait',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UnitSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('description', models.TextField()),
                ('wikipedia_url', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('acronym', models.CharField(max_length=5)),
                ('abbreviation', models.CharField(max_length=10)),
                ('wikipedia_url', models.CharField(blank=True, max_length=150, null=True)),
                ('quantity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='utility.quantity')),
                ('unit_system', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='utility.unitsystem')),
            ],
            options={
                'unique_together': {('unit_system', 'quantity', 'name')},
            },
        ),
        migrations.AddField(
            model_name='quantity',
            name='si_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='si_quantity', to='utility.unit'),
        ),
        migrations.CreateModel(
            name='KnowledgeGraph',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=250)),
                ('image_content_url', models.CharField(blank=True, max_length=250, null=True)),
                ('image_url', models.CharField(blank=True, max_length=500, null=True)),
                ('article_body', models.CharField(max_length=2000)),
                ('wikipedia', models.CharField(max_length=250)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.DO_NOTHING, related_name='knowledgegraph_created_by', to='identity.identity')),
                ('deleted_by', models.ForeignKey(blank=True, db_column='deleted_by', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='knowledgegraph_deleted_by', to='identity.identity')),
                ('last_modified_by', models.ForeignKey(blank=True, db_column='last_modified_by', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='knowledgegraph_last_modified', to='identity.identity')),
            ],
            options={
                'db_table': 'knowledge_graph',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('email_address', models.CharField(max_length=100, null=True)),
                ('url', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('feedback_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utility.feedbacktype')),
                ('identity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='identity.identity')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
