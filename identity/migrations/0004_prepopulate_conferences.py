# Generated by Django 2.2.11 on 2020-03-20 02:08

import csv
from datetime import datetime
from django.db import migrations
from django.contrib.auth.models import User
from identity import models
from sport import models as athletics_models


def create_entity(name, entity_type, creator, **kwargs):
    existing_entity = models.Entity.objects.filter(name=name, entity_type=entity_type).first()
    if not existing_entity:
        website = kwargs.get('website')
        entity = models.Entity(name=name, entity_type=entity_type, knowledge_graph_id=None, website=website, created_by=creator, slug=kwargs.get('slug'))
        entity.save()
    else:
        entity = existing_entity

    aliases = kwargs.get('aliases', [])
    for alias in aliases:
        if alias == aliases[0]:
            preferred = 1
        else:
            preferred = 0
        existing_aliases = models.EntityAlias.objects.filter(entity=entity, name=alias).exists()
        if not existing_aliases:
            alias_instance = models.EntityAlias(entity=entity, name=alias, preferred_indicator=preferred, created_by=creator)
            alias_instance.save()

    return entity


def create_identity(entity, name, identity_type, creator, **kwargs):
    existing_identity = models.Identity.objects.filter(name=name, identifier=name, identity_type=identity_type).first()
    if not existing_identity:
        identity = models.Identity(name=name, identifier=name, identity_type=identity_type, is_private=False, created_by=creator)
        identity.save()
    else:
        identity = existing_identity

    existing_entity_identity = models.EntityIdentity.objects.filter(entity=entity, identity=identity).first()
    if not existing_entity_identity:
        entity_identity = models.EntityIdentity(entity=entity, identity=identity, is_private=False, created_by=creator)
        entity_identity.save()

    organization_type = kwargs.get('organization_type')
    if organization_type:
        existing_identity_organizations = models.IdentityOrganization.objects.filter(identity=identity, organization_type=organization_type).all()
        if not existing_identity_organizations:
            formation_date = kwargs.get('formation_date')
            identity_organization = models.IdentityOrganization(identity=identity, organization_type=organization_type, formation_date=formation_date, created_by=creator)
            identity_organization.save()

    return identity


def create_entity_identity(name, entity_type, identity_type, creator, **kwargs):
    entity = create_entity(name, entity_type, creator, **kwargs)
    identity = create_identity(entity, name, identity_type, creator, **kwargs)
    return entity, identity


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0003_prepopulate_tables'),
    ]

    def create_naia(apps, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = models.Identity.objects.get(user_id=superuser.id)

        organization_entity_type = models.EntityType.objects.filter(name='Organization').first()
        identity_type = models.IdentityType.objects.filter(name='Organization').first()
        association_organization_type = models.OrganizationType.objects.filter(name='Association').first()
        association_name = 'National Association of Intercollegiate Athletics'
        association_acronym = 'NAIA'
        association_aliases = [association_name, association_acronym]
        naia_entity = create_entity(association_name, organization_entity_type, superuser_identity, aliases=association_aliases)
        naia_identity = create_identity(naia_entity, association_acronym, identity_type, superuser_identity, organization_type=association_organization_type)

        identity_university_organization_type = models.OrganizationType.objects.filter(name='University').first()
        with open('identity/migrations/college_conferences/NAIA_schools.csv', 'r') as input_file:
            data = list(csv.DictReader(input_file))
        conferences = set(row['Conference'] for row in data if row['Conference'])

        conference_organization_type = models.OrganizationType.objects.filter(name='Conference').first()
        conference_lookup = dict()
        for conference in conferences:
            conference_entity, conference_identity = create_entity_identity(conference, organization_entity_type, identity_type, superuser_identity, organization_type=conference_organization_type, aliases=[conference])
            conference_lookup[conference] = conference_identity

            existing_membership = models.OrganizationMembership.objects.filter(organization=naia_identity, member=conference_identity).all()
            if not existing_membership:
                start_date = datetime(1940, 1, 1)
                membership_instance = models.OrganizationMembership(organization=naia_identity, member=conference_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

        for row in data:
            school_name = row['School']
            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, organization_type=identity_university_organization_type, aliases=[school_name])

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
        association_aliases = [association_name, association_acronym]
        ncaa_entity = create_entity(association_name, organization_entity_type, superuser_identity, aliases=association_aliases)
        ncaa_identity = create_identity(ncaa_entity, association_acronym, identity_type, superuser_identity, organization_type=association_organization_type)

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

        conference_organization_type = models.OrganizationType.objects.filter(name='Conference').first()
        conference_lookup = dict()
        for conference in conferences:
            conference_entity, conference_identity = create_entity_identity(conference, organization_entity_type, identity_type, superuser_identity, organization_type=conference_organization_type, aliases=[conference])
            conference_lookup[conference] = conference_identity

            existing_membership = models.OrganizationMembership.objects.filter(organization=ncaa_identity, member=conference_identity).all()
            if not existing_membership:
                start_date = datetime(1906, 3, 31)
                membership_instance = models.OrganizationMembership(organization=ncaa_identity, member=conference_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

        for row in data:
            school_name = row['School']
            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, organization_type=identity_university_organization_type, aliases=[school_name])

            conference_name = row['Primary Conference']
            if not conference_name:
                continue
            conference = conference_lookup[conference_name]
            existing_membership = models.OrganizationMembership.objects.filter(organization=conference, member=school_identity).all()
            if not existing_membership:
                start_date = datetime(1906, 3, 31)
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
        association_aliases = [association_name, association_acronym]
        ncaa_entity = create_entity(association_name, organization_entity_type, superuser_identity, aliases=association_aliases)
        ncaa_identity = create_identity(ncaa_entity, association_acronym, identity_type, superuser_identity, organization_type=association_organization_type)

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
            conference_entity, conference_identity = create_entity_identity(conference, organization_entity_type, identity_type, superuser_identity, organization_type=conference_organization_type, aliases=[conference])
            conference_lookup[conference] = conference_identity

            existing_membership = models.OrganizationMembership.objects.filter(organization=ncaa_identity, member=conference_identity).all()
            if not existing_membership:
                start_date = datetime(1906, 3, 31)
                membership_instance = models.OrganizationMembership(organization=ncaa_identity, member=conference_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

        for row in data:
            school_name = row['School']
            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, organization_type=identity_university_organization_type, aliases=[school_name])

            conference_name = row['Conference']
            if not conference_name:
                continue
            conference = conference_lookup[conference_name]
            existing_membership = models.OrganizationMembership.objects.filter(organization=conference, member=school_identity).all()
            if not existing_membership:
                start_date = datetime(1906, 3, 31)
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
        association_aliases = [association_name, association_acronym]
        ncaa_entity = create_entity(association_name, organization_entity_type, superuser_identity, aliases=association_aliases)
        ncaa_identity = create_identity(ncaa_entity, association_acronym, identity_type, superuser_identity, organization_type=association_organization_type)

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

        conference_organization_type = models.OrganizationType.objects.filter(name='Conference').first()
        conference_lookup = dict()
        for conference in conferences:
            conference_entity, conference_identity = create_entity_identity(conference, organization_entity_type, identity_type, superuser_identity, organization_type=conference_organization_type)
            conference_lookup[conference] = conference_identity

            existing_membership = models.OrganizationMembership.objects.filter(organization=ncaa_identity, member=conference_identity).all()
            if not existing_membership:
                start_date = datetime(1906, 3, 31)
                membership_instance = models.OrganizationMembership(organization=ncaa_identity, member=conference_identity, division=division_instance, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

        for row in data:
            school_name = row['School']
            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, organization_type=identity_university_organization_type, aliases=[school_name])

            conference_name = row['Conference']
            if not conference_name:
                continue
            conference = conference_lookup[conference_name]
            existing_membership = models.OrganizationMembership.objects.filter(organization=conference, member=school_identity).all()
            if not existing_membership:
                start_date = datetime(1906, 3, 31)
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
        assocation_aliases = [association_name, association_acronym]
        nccaa_entity = create_entity(association_name, organization_entity_type, superuser_identity, aliases=assocation_aliases)
        nccaa_identity = create_identity(nccaa_entity, association_acronym, identity_type, superuser_identity, organization_type=association_organization_type)

        identity_university_organization_type = models.OrganizationType.objects.filter(name='University').first()
        with open('identity/migrations/college_conferences/NCCAA_schools.csv', 'r') as input_file:
            data = list(csv.DictReader(input_file))
        regions = set(row['Region'] for row in data if row['Region'])

        region_lookup = dict()
        for region in regions:
            region_name = '%s - %s' % (association_acronym, region)
            region_identity = create_identity(nccaa_entity, region_name, identity_type, superuser_identity, organization_type=association_organization_type)

            existing_membership = models.OrganizationMembership.objects.filter(organization=nccaa_identity, member=region_identity).all()
            if not existing_membership:
                start_date = datetime(1968, 1, 1)
                membership_instance = models.OrganizationMembership(organization=nccaa_identity, member=region_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()
            region_lookup[region] = region_identity

        for row in data:
            school_name = row['School']

            school_entity, school_identity = create_entity_identity(school_name, organization_entity_type, identity_type, superuser_identity, organization_type=identity_university_organization_type, aliases=[school_name])
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
                start_date = datetime(1968, 1, 1)
                membership_instance = models.OrganizationMembership(organization=region_identity, member=school_identity, division=division_instance, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

    def create_federations(app, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = models.Identity.objects.get(user_id=superuser.id)

        organization_entity_type = models.EntityType.objects.filter(name='Organization').first()
        identity_type = models.IdentityType.objects.filter(name='Organization').first()
        federation_organization_type = models.OrganizationType.objects.filter(name='Federation').first()

        global_federation = dict(name='World Athletics', aliases=['International Amateur Athletic Federation', 'International Association of Athletics Federations', 'IAAF'], formation=datetime(1912, 7, 17), website='www.worldathletics.org')

        global_federation_name = global_federation['name']
        global_federation_website = global_federation['website']
        global_federation_formation_date = global_federation['formation']
        global_federation_aliases = global_federation['aliases']
        global_federation_entity = create_entity(global_federation_name, organization_entity_type, superuser_identity, website=global_federation_website, aliases=global_federation_aliases)
        global_federation_identity = create_identity(global_federation_entity, global_federation_name, identity_type, superuser_identity, organization_type=federation_organization_type, formation_date=global_federation_formation_date)

        federations = [
            dict(name='Asian Athletics Association', aliases=['Asian Athletics Association', 'AAA'], formation=datetime(1912, 7, 17), website='www.athleticsasia.org'),
            dict(name='Confederation of African Athletics', aliases=['Confederation of African Athletics', 'CAA'], formation=datetime(1912, 7, 17), website='www.caaweb.org'),
            dict(name=u'Confederación Sudamericana de Atletismo', aliases=[u'Confederación Sudamericana de Atletismo', 'CONSUDATLE'], formation=datetime(1918, 1, 1), website='www.consudatle.org'),
            dict(name='European Athletic Association', aliases=['European Athletic Association', 'European Athletics', 'EAA'], formation=datetime(1969, 1, 1), website='www.european-athletics.org'),
            dict(name='North American, Central American and Caribbean Athletic Association', aliases=['North American, Central American and Caribbean Athletic Association', 'NACAC'], formation=datetime(1988, 1, 1), website='www.athleticsnacac.org'),
            dict(name='Oceania Athletics Association', aliases=['Oceania Athletics Association', 'OAA'], formation=datetime(1969, 8, 21), website='www.athletics-oceania.com'),
        ]

        regional_federation_lookup = dict()
        for federation in federations:
            federation_name = federation['name']
            federation_website = federation['website']
            formation_date = federation['formation']
            federation_aliases = federation['aliases']
            federation_entity = create_entity(federation_name, organization_entity_type, superuser_identity, website=federation_website, aliases=federation_aliases)
            federation_identity = create_identity(federation_entity, federation_name, identity_type, superuser_identity, organization_type=federation_organization_type, formation_date=formation_date)
            regional_federation_lookup[federation_aliases[-1]] = federation_identity
            start_date = max(global_federation_formation_date, formation_date)
            existing_membership = models.OrganizationMembership.objects.filter(organization=global_federation_identity, member=federation_identity).all()
            if not existing_membership:
                membership_instance = models.OrganizationMembership(organization=global_federation_identity, member=federation_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()

        with open('identity/migrations/federations.csv', 'r') as input_file:
            data = list(csv.DictReader(input_file))

        for row in data:
            federation_name = row['name']
            if not federation_name.strip():
                continue
            federation_website = row['website']
            federation_acronym = row['abbreviation']
            aliases = [federation_name]
            if federation_acronym:
                aliases.append(federation_acronym)

            federation_entity = create_entity(federation_name, organization_entity_type, superuser_identity, website=federation_website, aliases=aliases)

            raw_founded_date = row['founded']
            if raw_founded_date and raw_founded_date.count('/') == 2:
                founded_date = datetime.strptime(raw_founded_date, '%m/%d/%Y')
            elif raw_founded_date and not raw_founded_date.count('/'):
                founded_date = datetime.strptime(raw_founded_date, '%Y')
            else:
                founded_date = None

            federation_identity = create_identity(federation_entity, federation_name, identity_type, superuser_identity, organization_type=federation_organization_type, formation_date=founded_date)

            raw_affiliation_date = row['Affiliation Date']
            if raw_affiliation_date and raw_affiliation_date.count('/') == 2:
                affiliation_date = datetime.strptime(raw_affiliation_date, '%m/%d/%Y')
            elif raw_affiliation_date and not raw_affiliation_date.count('/'):
                affiliation_date = datetime.strptime(raw_affiliation_date, '%Y')
            else:
                affiliation_date = None

            region_federation_acronym = row['regional affiliation']
            if region_federation_acronym not in regional_federation_lookup:
                continue
            region_federation_identity = regional_federation_lookup[region_federation_acronym]
            existing_membership = models.OrganizationMembership.objects.filter(organization=region_federation_identity, member=federation_identity).all()
            if not existing_membership:
                if affiliation_date:
                    start_date = affiliation_date
                elif not affiliation_date and founded_date:
                    start_date = founded_date
                else:
                    start_date = global_federation_formation_date
                membership_instance = models.OrganizationMembership(organization=region_federation_identity, member=federation_identity, start_date=start_date, created_by=superuser_identity)
                membership_instance.save()


    operations = [
        migrations.RunPython(create_naia),
        migrations.RunPython(create_ncaa_d1),
        migrations.RunPython(create_ncaa_d2),
        migrations.RunPython(create_ncaa_d3),
        migrations.RunPython(create_nccaa),
        migrations.RunPython(create_federations)
    ]
