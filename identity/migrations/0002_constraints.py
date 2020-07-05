# Generated by Django 2.2.11 on 2020-07-04 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utility', '0001_initial'),
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='knowledge_graph',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='utility.KnowledgeGraph'),
        ),
        migrations.AddField(
            model_name='entity',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, db_column='last_modified_by', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='last_modified_entities', to='identity.Identity'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='created_by',
            field=models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_attributes', to='identity.Identity'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, db_column='last_modified_by', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='last_modified_attributes', to='identity.Identity'),
        ),
        migrations.AlterUniqueTogether(
            name='stagingidentityorganization',
            unique_together={('staging_identity', 'organization_type', 'headquarters_location')},
        ),
        migrations.AlterUniqueTogether(
            name='stagingidentity',
            unique_together={('organization', 'identifier')},
        ),
        migrations.AlterUniqueTogether(
            name='organizationmembership',
            unique_together={('organization', 'member')},
        ),
        migrations.AlterUniqueTogether(
            name='identitytrait',
            unique_together={('identity', 'trait')},
        ),
        migrations.AlterUniqueTogether(
            name='identityorganization',
            unique_together={('identity', 'organization_type', 'headquarters_location')},
        ),
        migrations.AlterUniqueTogether(
            name='identitycitizenship',
            unique_together={('identity', 'country')},
        ),
        migrations.AlterUniqueTogether(
            name='identityattribute',
            unique_together={('identity', 'attribute')},
        ),
        migrations.AlterUniqueTogether(
            name='identity',
            unique_together={('organization', 'identifier')},
        ),
        migrations.AlterUniqueTogether(
            name='entitytrait',
            unique_together={('entity', 'trait')},
        ),
        migrations.AlterUniqueTogether(
            name='entityidentity',
            unique_together={('entity', 'identity')},
        ),
        migrations.AlterUniqueTogether(
            name='entityattribute',
            unique_together={('entity', 'attribute')},
        ),
    ]
