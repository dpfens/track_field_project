# Generated by Django 2.2.11 on 2020-03-20 02:08

import csv
from datetime import datetime
from django.db import migrations
from django.contrib.auth.models import User
from identity import models
from athletics import models as athletics_models


def create_entity(name, entity_type, creator):
    existing_entity = models.Entity.objects.filter(name=name, entity_type=entity_type).all()
    if not existing_entity:
        entity = models.Entity(name=name, entity_type=entity_type, knowledge_graph_id=None, created_by=creator)
        entity.save()
    else:
        entity = existing_entity[0]
    return entity


def create_identity(entity, name, identity_type, creator, organization_type=None):
    existing_identity = models.Identity.objects.filter(name=name, identifier=name, identity_type=identity_type).all()
    if not existing_identity:
        identity = models.Identity(name=name, identifier=name, identity_type=identity_type, is_private=False, created_by=creator)
        identity.save()
    else:
        identity = existing_identity[0]

    existing_entity_identity = models.EntityIdentity.objects.filter(entity=entity, identity=identity).all()
    if not existing_entity_identity:
        entity_identity = models.EntityIdentity(entity=entity, identity=identity, is_private=False, created_by=creator)
        entity_identity.save()

    if organization_type:
        existing_identity_organizations = models.IdentityOrganization.objects.filter(identity=identity, organization_type=organization_type).all()
        if not existing_identity_organizations:
            identity_organization = models.IdentityOrganization(identity=identity, organization_type=organization_type, created_by=creator)
            identity_organization.save()

    return identity


def create_entity_identity(name, entity_type, identity_type, creator, organization_type=None):
    entity = create_entity(name, entity_type, creator)
    identity = create_identity(entity, name, identity_type, creator, organization_type)

    return entity, identity


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
    ]

    def create_naia(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = models.Identity.objects.get(user_id=superuser.id)

        organization_entity_type = models.EntityType.objects.filter(name='Organization').first()
        identity_type = models.IdentityType.objects.filter(name='Organization').first()
        association_organization_type = models.OrganizationType.objects.filter(name='Association').first()
        association_name = 'National Association of Intercollegiate Athletics'
        association_acronym = 'NAIA'
        naia_entity = create_entity(association_name, organization_entity_type, superuser_identity)
        naia_identity = create_identity(naia_entity, association_acronym, identity_type, superuser_identity, association_organization_type)

        identity_university_organization_type = models.OrganizationType.objects.filter(name='University').first()
        with open('identity/migrations/college_conferences/NAIA_schools.csv', 'r') as input_file:
            data = list(csv.DictReader(input_file))
        conferences = set(row['Conference'] for row in data if row['Conference'])

        conference_organization_type = models.OrganizationType.objects.filter(name='Conference').first()
        conference_lookup = dict()
        for conference in conferences:
            conference_entity, conference_identity = create_entity_identity(conference, organization_entity_type, identity_type, superuser_identity, conference_organization_type)
            conference_lookup[conference] = conference_identity

            existing_membership = models.OrganizationMembership.objects.filter(organization=naia_identity, member=conference_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=naia_identity, member=conference_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

        for row in data:
            school_name = row['School']
            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, identity_university_organization_type)

            conference_name = row['Conference']
            if not conference_name:
                continue
            conference = conference_lookup[conference_name]
            existing_membership = models.OrganizationMembership.objects.filter(organization=conference, member=school_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=conference, member=school_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

    def create_ncaa_d1(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = models.Identity.objects.get(user_id=superuser.id)

        organization_entity_type = models.EntityType.objects.filter(name='Organization').first()
        identity_type = models.IdentityType.objects.filter(name='Organization').first()
        association_organization_type = models.OrganizationType.objects.filter(name='Association').first()
        association_name = 'National Collegiate Athletic Association'
        association_acronym = 'NCAA'
        ncaa_entity = create_entity(association_name, organization_entity_type, superuser_identity)
        ncaa_identity = create_identity(ncaa_entity, association_acronym, identity_type, superuser_identity, association_organization_type)

        identity_university_organization_type = models.OrganizationType.objects.filter(name='University').first()
        with open('identity/migrations/college_conferences/NCAA_D1_schools.csv', 'r') as input_file:
            data = list(csv.DictReader(input_file))
        conferences = set(row['Primary Conference'] for row in data if row['Primary Conference'])

        existing_divisions = athletics_models.Division.objects.filter(organization=ncaa_identity, name=1).all()
        if not existing_divisions:
            division_instance = athletics_models.Division(organization=ncaa_identity, name=1, description='', created_by=superuser_identity)
            division_instance.save()
        else:
            division_instance = existing_divisions[0]
        # TODO: Associate an organization with a division

        conference_organization_type = models.OrganizationType.objects.filter(name='Conference').first()
        conference_lookup = dict()
        for conference in conferences:
            conference_entity, conference_identity = create_entity_identity(conference, organization_entity_type, identity_type, superuser_identity, conference_organization_type)
            conference_lookup[conference] = conference_identity

            existing_membership = models.OrganizationMembership.objects.filter(organization=ncaa_identity, member=conference_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=ncaa_identity, member=conference_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

        for row in data:
            school_name = row['School']
            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, identity_university_organization_type)

            conference_name = row['Primary Conference']
            if not conference_name:
                continue
            conference = conference_lookup[conference_name]
            existing_membership = models.OrganizationMembership.objects.filter(organization=conference, member=school_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=conference, member=school_identity, division=division_instance, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

    def create_ncaa_d2(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = models.Identity.objects.get(user_id=superuser.id)

        organization_entity_type = models.EntityType.objects.filter(name='Organization').first()
        identity_type = models.IdentityType.objects.filter(name='Organization').first()
        association_organization_type = models.OrganizationType.objects.filter(name='Association').first()

        association_name = 'National Collegiate Athletic Association'
        association_acronym = 'NCAA'
        ncaa_entity = create_entity(association_name, organization_entity_type, superuser_identity)
        ncaa_identity = create_identity(ncaa_entity, association_acronym, identity_type, superuser_identity, association_organization_type)

        identity_university_organization_type = models.OrganizationType.objects.filter(name='University').first()
        with open('identity/migrations/college_conferences/NCAA_D2_schools.csv', 'r') as input_file:
            data = list(csv.DictReader(input_file))
        conferences = set(row['Conference'] for row in data if row['Conference'])

        existing_divisions = athletics_models.Division.objects.filter(organization=ncaa_identity, name=1).all()
        if not existing_divisions:
            division_instance = athletics_models.Division(organization=ncaa_identity, name=2, created_by=superuser_identity)
            division_instance.save()
        else:
            division_instance = existing_divisions[0]

        conference_organization_type = models.OrganizationType.objects.filter(name='Conference').first()
        conference_lookup = dict()
        for conference in conferences:
            conference_entity, conference_identity = create_entity_identity(conference, organization_entity_type, identity_type, superuser_identity, conference_organization_type)
            conference_lookup[conference] = conference_identity

            existing_membership = models.OrganizationMembership.objects.filter(organization=ncaa_identity, member=conference_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=ncaa_identity, member=conference_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

        for row in data:
            school_name = row['School']
            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, identity_university_organization_type)

            conference_name = row['Conference']
            if not conference_name:
                continue
            conference = conference_lookup[conference_name]
            existing_membership = models.OrganizationMembership.objects.filter(organization=conference, member=school_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=conference, member=school_identity, division=division_instance, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

    def create_ncaa_d3(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = models.Identity.objects.get(user_id=superuser.id)

        organization_entity_type = models.EntityType.objects.filter(name='Organization').first()
        identity_type = models.IdentityType.objects.filter(name='Organization').first()
        association_organization_type = models.OrganizationType.objects.filter(name='Association').first()

        association_name = 'National Collegiate Athletic Association'
        association_acronym = 'NCAA'
        ncaa_entity = create_entity(association_name, organization_entity_type, superuser_identity)
        ncaa_identity = create_identity(ncaa_entity, association_acronym, identity_type, superuser_identity, association_organization_type)

        identity_university_organization_type = models.OrganizationType.objects.filter(name='University').first()
        with open('identity/migrations/college_conferences/NCAA_D3_schools.csv', 'r') as input_file:
            data = list(csv.DictReader(input_file))
        conferences = set(row['Conference'] for row in data if row['Conference'])

        existing_divisions = athletics_models.Division.objects.filter(organization=ncaa_identity, name=1).all()
        if not existing_divisions:
            division_instance = athletics_models.Division(organization=ncaa_identity, name=3, created_by=superuser_identity)
            division_instance.save()
        else:
            division_instance = existing_divisions[0]
        # TODO: Associate an organization with a division

        conference_organization_type = models.OrganizationType.objects.filter(name='Conference').first()
        conference_lookup = dict()
        for conference in conferences:
            conference_entity, conference_identity = create_entity_identity(conference, organization_entity_type, identity_type, superuser_identity, conference_organization_type)
            conference_lookup[conference] = conference_identity

            existing_membership = models.OrganizationMembership.objects.filter(organization=ncaa_identity, member=conference_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=ncaa_identity, member=conference_identity, division=division_instance, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

        for row in data:
            school_name = row['School']
            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, identity_university_organization_type)

            conference_name = row['Conference']
            if not conference_name:
                continue
            conference = conference_lookup[conference_name]
            existing_membership = models.OrganizationMembership.objects.filter(organization=conference, member=school_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=conference, member=school_identity, division=division_instance, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

    def create_nccaa(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = models.Identity.objects.get(user_id=superuser.id)

        organization_entity_type = models.EntityType.objects.filter(name='Organization').first()
        identity_type = models.IdentityType.objects.filter(name='Organization').first()
        association_organization_type = models.OrganizationType.objects.filter(name='Association').first()
        association_name = 'National Christian College Athletic Association'
        association_acronym = 'NCCAA'
        nccaa_entity = create_entity(association_name, organization_entity_type, superuser_identity)
        nccaa_identity = create_identity(nccaa_entity, association_acronym, identity_type, superuser_identity, association_organization_type)

        identity_university_organization_type = models.OrganizationType.objects.filter(name='University').first()
        with open('identity/migrations/college_conferences/NCCAA_schools.csv', 'r') as input_file:
            data = list(csv.DictReader(input_file))
        regions = set(row['Region'] for row in data if row['Region'])

        region_lookup = dict()
        for region in regions:
            region_name = '%s - %s' % (association_acronym, region)
            region_identity = create_identity(nccaa_entity, region_name, identity_type, superuser_identity, association_organization_type)

            existing_membership = models.OrganizationMembership.objects.filter(organization=nccaa_identity, member=region_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=nccaa_identity, member=region_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()
            region_lookup[region] = region_identity

        for row in data:
            school_name = row['School']

            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, identity_university_organization_type)
            region = row['Region']
            region_identity = region_lookup[region]

            division = row['Division']
            existing_divisions = athletics_models.Division.objects.filter(organization=region_identity, name=division).all()
            if not existing_divisions:
                division_instance = athletics_models.Division(organization=region_identity, name=division, created_by=superuser_identity)
                division_instance.save()
            else:
                division_instance = existing_divisions[0]

            existing_membership = models.OrganizationMembership.objects.filter(organization=region_identity, member=school_identity).all()
            if not existing_membership:
                start_date = datetime(1900, 1, 1)
                membership_instance = models.OrganizationMembership(organization=region_identity, member=school_identity, division=division_instance, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

    operations = [
        migrations.RunPython(create_naia),
        migrations.RunPython(create_ncaa_d1),
        migrations.RunPython(create_ncaa_d2),
        migrations.RunPython(create_ncaa_d3),
        migrations.RunPython(create_nccaa)
    ]
