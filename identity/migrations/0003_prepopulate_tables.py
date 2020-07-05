# Generated by Django 2.2.9 on 2020-01-12 18:56

from django.db import migrations
from identity import models
from django.contrib.auth.models import User
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0002_constraints'),
        ('auth', '0005_alter_user_last_login_null')
    ]

    def create_entity_types(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        identity = models.Identity.objects.get(user_id=superuser.id)
        types = ['Person', 'Organization', 'Government', 'Bot', 'Relay']
        for type in types:
            try:
                models.EntityType.objects.get(name=type)
            except Exception:
                entity_type = models.EntityType(name=type, description='', created_by=identity)
                entity_type.save()

    def create_identity_types(apps, schema_editor):
        types = ['Anonymous User', 'User', 'Person', 'Organization', 'Bot', 'Relay']
        for type in types:
            try:
                models.IdentityType.objects.get(name=type)
            except Exception:
                identity_type = models.IdentityType(name=type, description='', created_by=None)
                identity_type.save()

    def create_organization_types(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        identity = models.Identity.objects.get(user_id=superuser.id)

        types = ['Business', 'Federation', 'Government', 'Association', 'Committee', 'Conference', 'University',  'Club']
        for type in types:
            try:
                models.OrganizationType.objects.get(name=type)
            except Exception:
                organization_type = models.OrganizationType(name=type, description='', created_by=identity)
                organization_type.save()

    def create_organization(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = models.Identity.objects.get(user_id=superuser.id)

        now = datetime.now()
        organization_identity_type = models.IdentityType.objects.get(name='User')
        try:
            organization_identity = models.Identity.objects.get(identity_type=organization_identity_type, is_private=False, identifier=0, created_by=superuser_identity)
        except Exception:
            organization_identity = models.Identity(identity_type=organization_identity_type, is_private=False, identifier=0, created_by=superuser_identity)
            organization_identity.save()

        organization_type = models.OrganizationType.objects.get(name='Business')
        try:
            organization = models.IdentityOrganization.objects.get(identity=organization_identity, organization_type=organization_type, formation_date=now, created_by=superuser_identity)
        except Exception:
            organization = models.IdentityOrganization(identity=organization_identity, organization_type=organization_type, formation_date=now, created_by=superuser_identity)
            organization.save()

        entity_type = models.EntityType.objects.get(name='Organization')
        try:
            entity = models.Entity.objects.get(name='Business Name', entity_type=entity_type, knowledge_graph_id=None, created_by=superuser_identity)
        except Exception:
            entity = models.Entity(name='Business Name', entity_type=entity_type, knowledge_graph_id=None, created_by=superuser_identity)
            entity.save()

        try:
            entity_identity = models.EntityIdentity(entity=entity, identity=organization_identity, created_by=superuser_identity, is_private=False)
        except Exception:
            entity_identity = models.EntityIdentity(entity=entity, identity=organization_identity, created_by=superuser_identity, is_private=False)
            entity_identity.save()

    def create_genders(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = models.Identity.objects.get(user_id=superuser.id)
        genders = ('Male', 'Female')
        for gender_name in genders:
            gender = models.Gender.objects.filter(name=gender_name).first()
            if not gender:
                gender = models.Gender(name=gender_name, description='', created_by=superuser_identity)
                gender.save()

    def create_superuser(apps, schema_editor):
        user_name = input('username for superuser:')
        try:
            superuser = User.objects.get(username=user_name)
        except Exception as e:
            print(e)
            email = input('Email address for superuser %r:' % user_name)
            password = input('Password for superuser %r:' % user_name)
            superuser = User.objects.create_superuser(user_name, email, password)
            superuser.save()


        identity_type = models.IdentityType.objects.get(name='User')
        try:
            models.Identity.objects.get(user=superuser, identity_type=identity_type, is_private=False, identifier=superuser.id, created_by=None)
        except Exception:
            superuser_identity = models.Identity(user=superuser, identity_type=identity_type, is_private=False, identifier=superuser.id, created_by=None)
            superuser_identity.save()
            print('created %r' % superuser_identity)

    operations = [
        migrations.RunPython(create_identity_types),
        migrations.RunPython(create_superuser),
        migrations.RunPython(create_entity_types),
        migrations.RunPython(create_organization_types),
        migrations.RunPython(create_organization),
        migrations.RunPython(create_genders)
    ]
