# Generated by Django 2.2.11 on 2020-03-21 22:40

from django.db import migrations
from datetime import datetime
from athletics import models
from django.contrib.auth.models import User
from identity import models as identity_models
from geography import models as geography_models
import json


def parse_time(text):
    multipliers = (1.0, 60.0, 3600.0)
    parts = text.split(':')
    part_count = len(parts)
    output = 0.0
    for i in range(part_count - 1, -1, -1):
        part = float(parts[i])
        multiplier = multipliers[i]
        output += part * multiplier
    return output


def create_entity(name, entity_type, creator, **kwargs):
    existing_entity = identity_models.Entity.objects.filter(name=name, entity_type=entity_type).all()
    if not existing_entity:
        website = kwargs.get('website')
        entity = identity_models.Entity(name=name, entity_type=entity_type, knowledge_graph_id=None, website=website, created_by=creator)
        entity.save()
    else:
        entity = existing_entity[0]

    aliases = kwargs.get('aliases', [])
    for alias in aliases:
        if alias == aliases[0]:
            preferred = 1
        else:
            preferred = 0
        existing_aliases = identity_models.EntityAlias.objects.filter(entity=entity, name=alias).all()
        if not existing_aliases:
            alias_instance = identity_models.EntityAlias(entity=entity, name=alias, preferred_indicator=preferred, created_by=creator)
            alias_instance.save()

    return entity


def create_identity(entity, id, name, identity_type, creator, **kwargs):
    existing_identity = identity_models.Identity.objects.filter(name=name, identifier=name, identity_type=identity_type).all()
    if not existing_identity:
        organization = kwargs.get('organization')
        identity = identity_models.Identity(organization=organization, name=name, identifier=id, identity_type=identity_type, is_private=False, created_by=creator)
        identity.save()
    else:
        identity = existing_identity[0]

    existing_entity_identity = identity_models.EntityIdentity.objects.filter(entity=entity, identity=identity).all()
    if not existing_entity_identity:
        entity_identity = identity_models.EntityIdentity(entity=entity, identity=identity, is_private=False, created_by=creator)
        entity_identity.save()

    organization_type = kwargs.get('organization_type')
    if organization_type:
        existing_identity_organizations = identity_models.IdentityOrganization.objects.filter(identity=identity, organization_type=organization_type).all()
        if not existing_identity_organizations:
            formation_date = kwargs.get('formation_date')
            identity_organization = identity_models.IdentityOrganization(identity=identity, organization_type=organization_type, formation_date=formation_date, created_by=creator)
            identity_organization.save()

    return identity


def create_entity_identity(name, entity_type, identity_type, creator, **kwargs):
    entity = create_entity(name, entity_type, creator, **kwargs)
    identity = create_identity(entity, name, identity_type, creator, **kwargs)
    return entity, identity


class Migration(migrations.Migration):

    dependencies = [
        ('athletics', '0001_initial'),
    ]

    def create_open_meet(app, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = identity_models.Identity.objects.get(user_id=superuser.id)

        outdoor_environment = models.Environment.objects.filter(name='Outdoor').first()
        if not outdoor_environment:
            outdoor_environment = models.Environment(name='Outdoor', description='', created_by=superuser_identity)
            outdoor_environment.save()

        meet_type = models.MeetType.objects.filter(name='Road Race').first()
        if not meet_type:
            meet_type = models.MeetType(name='Road Race', description='', created_by=superuser_identity)
            meet_type.save()

        meet_name = 'Valencia Marathon'
        meet = models.Meet.objects.filter(name=meet_name).first()
        if not meet:
            meet = models.Meet(meet_type=meet_type, environment=outdoor_environment, name=meet_name, slug='valencia-marathon', description='', championship=False, created_by=superuser_identity)
            meet.save()

        venue = geography_models.Venue.objects.filter(name='Valencia').first()
        if not venue:
            venue = geography_models.Venue(name='Valencia', slug='valencia', created_by=superuser_identity)
            venue.save()

        meet_start_date = datetime(2014, 12, 1)
        meet_end_date = datetime(2014, 12, 3)
        meet_url = 'https://www.valenciaciudaddelrunning.com/en/marathon/previous-editions-marathon/ranking-marathon-2014/'
        meet_instance = models.MeetInstance.objects.filter(name="2014 Valencia Marathon").first()
        if not meet_instance:
            meet_instance = models.MeetInstance(meet=meet, venue=venue, name="2014 Valencia Marathon", slug='2014-valencia-marathon', start_date=meet_start_date, end_date=meet_end_date, url=meet_url, participants=0, created_by=superuser_identity)
            meet_instance.save()

        marathon_event = models.Event.objects.filter(name='Marathon').first()
        competition_type = models.CompetitionType.objects.filter(name='Race').first()

        competition = models.Competition.objects.filter(meet_instance=meet_instance, event=marathon_event, name='Marathon', slug='2014-valencia-marathon').first()
        if not competition:
            competition = models.Competition(competition_type=competition_type, meet_instance=meet_instance, event=marathon_event, name='Marathon', slug='2014-valencia-marathon', url='', participants=0, created_by=superuser_identity)
            competition.save()

        tier = models.Tier.objects.filter(name='Finals').first()

        heat = models.Heat.objects.filter(competition=competition, name='Open').first()
        if not heat:
            heat = models.Heat(competition=competition, tier=tier, name='Open', description='', overall=True, created_by=superuser_identity)
            heat.save()

        finished_performance_state = models.PerformanceState.objects.filter(code='FINISH').first()
        verified_legitimacy = models.Legitimacies.objects.filter(name='Verified').first()

        person_entity_type = identity_models.EntityType.objects.filter(name='Person').first()
        person_identity_type = identity_models.IdentityType.objects.filter(name='Person').first()

        org_entity_type = identity_models.EntityType.objects.filter(name='Organization').first()
        org_identity_type = identity_models.IdentityType.objects.filter(name='Organization').first()
        club_org_type = identity_models.OrganizationType.objects.filter(name='Club').first()

        file_name = 'athletics/migrations/meets/open_meet.json'
        with open(file_name, 'r') as input_file:
            data = json.load(input_file)
        total_rows = len(data)

        for index, row in enumerate(data):
            if index % 50 == 0:
                print('Uploading row %i of %i' % (index + 1, total_rows))
            club = row['Club']
            place = row['Position']
            id = row['id']
            bib = row['Dorsal']
            raw_time = row['Tiempo Oficial']
            raw_name = row['Number']
            middle_name = None
            if ',' in raw_name:
                last_name, first_middle_name = raw_name.split(',')
                first_middle_name_parts = first_middle_name.split()
                if len(first_middle_name_parts) > 1:
                    first_name, middle_name = first_middle_name.split(' ', 1)
                    middle_name = middle_name.strip()
                else:
                    first_name, middle_name = first_middle_name, None
            else:
                first_name, last_name = raw_name.split(' ', 1)
            first_name = first_name.strip()
            last_name = last_name.strip()

            person_entity = create_entity(raw_name, person_entity_type, superuser_identity, aliases=[raw_name])
            person_identity = create_identity(person_entity, id, raw_name, person_identity_type, superuser_identity)

            identity_person = identity_models.IdentityPerson.objects.filter(identity=person_identity).first()
            if not identity_person:
                if 'MASC' in club:
                    gender = identity_models.Gender.objects.filter(name='Male').first()
                else:
                    gender = identity_models.Gender.objects.filter(name='Female').first()
                identity_person = identity_models.IdentityPerson(identity=person_identity, gender=gender, given_name=first_name, middle_name=middle_name, last_name=last_name, created_by=superuser_identity)
                identity_person.save()

            if club != 'INDEPENDIENTE':
                club_entity = create_entity(club, org_entity_type, superuser_identity, aliases=[club])
                club_identity = create_identity(club_entity, club, club, org_identity_type, superuser_identity, organization_type=club_org_type)
            else:
                club_identity = None

            performance = models.Performance.objects.filter(heat=heat, organization=club_identity, identity=person_identity).first()
            if not performance:
                time = parse_time(raw_time)
                performance = models.Performance(heat=heat, organization=club_identity, identity=person_identity, value=time, bib=bib, place=place, points=None, state=finished_performance_state, legitimacy=verified_legitimacy, created_by=superuser_identity)
                performance.save()


    def create_track_field_race(app, schema_editor):
        file_name = 'athletics/migrations/meets/open_meet.json'

    def create_track_field_field(app, schema_editor):
        file_name = 'athletics/migrations/meets/open_meet.json'

    def create_track_field_relay(app, schema_editor):
        superuser = User.objects.filter(is_superuser=True).first()
        superuser_identity = identity_models.Identity.objects.get(user_id=superuser.id)

        federation_identity = identity_models.Identity.objects.filter(name='European Athletics Association').first()

        category = models.Category.objects.filter(name='European Athletics Events').first()
        if not category:
            category = models.Category(name='European Athletics Events', description='', created_by=superuser_identity)
            category.save()

        meet_type = models.MeetType.objects.filter(name='Track & Field').first()
        if not meet_type:
            meet_type = models.MeetType(name='Track & Field', description='', created_by=superuser_identity)
            meet_type.save()

        indoor_environment = models.Environment.objects.filter(name='Indoor').first()
        if not indoor_environment:
            indoor_environment = models.Environment(name='Indoor', description='', created_by=superuser_identity)
            indoor_environment.save()

        meet = models.Meet.objects.filter(meet_type=meet_type, environment=indoor_environment, name="European Athletics Indoor Championships", championship=1).first()
        if not meet:
            meet = models.Meet(meet_type=meet_type, organization=federation_identity, environment=indoor_environment, name="European Athletics Indoor Championships", description='', championship=1, created_by=superuser_identity)
            meet.save()

        venue = geography_models.Venue.objects.filter(name='Wien').first()
        if not venue:
            venue = geography_models.Venue(name='Wien', created_by=superuser_identity)
            venue.save()

        meet_start_date = datetime(2002, 3, 1)
        meet_end_date = datetime(2002, 3, 3)
        meet_url = "http://www.european-athletics.org/competitions/european-athletics-indoor-championships/history/year=2002/results/index.html"
        meet_instance = models.MeetInstance.objects.filter(meet=meet, venue=venue, name="27th European Athletics Indoor Championships").first()
        if not meet_instance:
            meet_instance = models.MeetInstance(meet=meet, venue=venue, name="27th European Athletics Indoor Championships", start_date=meet_start_date, end_date=meet_end_date, url=meet_url, participants=0, created_by=superuser_identity)
            meet_instance.save()

        run_mode = models.Mode.objects.filter(name='Run').first()
        event = models.Event.objects.filter(name='4 x 400m Relay').first()
        competition_type = models.CompetitionType.objects.filter(name='Race').first()
        competition = models.Competition.objects.filter(meet_instance=meet_instance, event=event, mode=run_mode, name='4 x 400m Men', slug='4-400m-men').first()
        if not competition:
            competition = models.Competition(competition_type=competition_type, meet_instance=meet_instance, event=event, mode=run_mode, name='4 x 400m Men', slug='4-400m-men', description='', url=meet_url, participants=0, created_by=superuser_identity)
            competition.save()

        finals_tier = models.Tier.objects.filter(name='Finals').first()
        heat = models.Heat.objects.filter(competition=competition, tier=finals_tier).first()
        if not heat:
            heat = models.Heat(competition=competition, tier=finals_tier, name='Overall', description='', overall=True, created_by=superuser_identity)
            heat.save()

        org_entity_type = identity_models.EntityType.objects.filter(name='Organization').first()
        org_identity_type = identity_models.IdentityType.objects.filter(name='Organization').first()
        team_entity = create_entity('Poland', org_entity_type, superuser_identity)
        team_identity = create_identity(team_entity, 'POL', 'Poland', org_identity_type, superuser_identity)
        relay_identity_type = identity_models.IdentityType.objects.filter(name='Relay').first()
        relay_identity = create_identity(team_entity,  'Poland1', 'Poland', relay_identity_type, superuser_identity, organization=team_identity)

        verified_legitimacy = models.Legitimacies.objects.filter(name='Verified').first()
        finished_performance_state = models.PerformanceState.objects.filter(code='FINISH').first()

        performance = models.Performance.objects.filter(heat=heat, identity=relay_identity, organization=team_identity).first()
        if not performance:
            performance = models.Performance(heat=heat, identity=relay_identity, organization=team_identity, place=1, points=0, value=185.5, reaction_time=None, wind=None, state=finished_performance_state, legitimacy=verified_legitimacy, created_by=superuser_identity)
            performance.save()

        athlete_data = [
            {
                "weight": {
                    "value": 65,
                    "units": "kg"
                },
                "id": 194706,
                "url": "http://www.european-athletics.org/athletes/group=g/athlete=194706-gasiewski-artur/index.html",
                "text": "Artur G\u0105siewski",
                "age": "",
                "height": {
                    "value": 176,
                    "units": "cm"
                },
                "born": datetime(1973, 11, 1),
                "team": "RKS Skra Warszawa"
            },
            {
                "id": 143520,
                "url": "https://www.european-athletics.org/athletes/group=p/athlete=143520-plawgo-marek/index.html",
                "text": "Marek Plawgo"
            },
            {
                "id": 200992,
                "url": "https://www.european-athletics.org/athletes/group=r/athlete=200992-rysiukiewicz-piotr/index.html",
                "text": "Piotr Rysiukiewicz"
            },
            {
                "id": 188474,
                "url": "https://www.european-athletics.org/athletes/group=m/athlete=188474-mackowiak-robert/index.html",
                "text": "Robert Maćkowiak"
            }
        ]

        entity_type = identity_models.EntityType.objects.filter(name='Person').first()
        identity_type = identity_models.IdentityType.objects.filter(name='Person').first()
        gender = identity_models.Gender.objects.filter(name='Male').first()
        athletes = []
        for index, athlete in enumerate(athlete_data):
            name = athlete['text']
            athlete_id = athlete['id']
            athlete_entity = create_entity(name, entity_type, superuser_identity)
            athlete_identity = create_identity(athlete_entity, athlete_id, name, identity_type, superuser_identity)
            athlete_person = identity_models.IdentityPerson.objects.filter(identity=athlete_identity).first()
            if not athlete_person:
                first_name, last_name = name.split()
                born = athlete.get('born')
                athlete_person = identity_models.IdentityPerson(identity=athlete_identity, gender=gender, given_name=first_name, last_name=last_name, date_of_birth=born, created_by=superuser_identity)
                athlete_person.save()

            relay_member = models.RelayMember.objects.filter(relay=relay_identity, identity=athlete_identity).first()
            if not relay_member:
                relay_member = models.RelayMember(relay=relay_identity, identity=athlete_identity, is_alternate=False, created_by=superuser_identity)
                relay_member.save()
            relay_performance_participant = models.RelayPerformanceParticipant.objects.filter(relay=relay_identity, member=athlete_identity, performance=performance).first()
            if not relay_performance_participant:
                relay_performance_participant = models.RelayPerformanceParticipant(relay=relay_identity, member=athlete_identity, performance=performance, sequence=index + 1, created_by=superuser_identity)
                relay_performance_participant.save()
            athletes.append(athlete_identity)

    operations = [
        migrations.RunPython(create_open_meet),
        migrations.RunPython(create_track_field_relay),
    ]
