# Generated by Django 2.2.9 on 2020-01-12 18:52

from django.db import migrations
import analytics
import identity
from django.contrib.auth.models import User


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial')
    ]

    def create_request_types(apps, schema_editor):
        superusers = User.objects.filter(is_superuser=True).all()
        superuser = superusers[0]
        superuser_identity = identity.models.Identity.objects.get(user_id=superuser.id)

        request_types = ['HTTP', 'HTTPS', 'GRPC']
        for name in request_types:
            try:
                instance = analytics.models.RequestType.objects.get(name=name)
            except Exception:
                instance = analytics.models.RequestType(name=name, description='', created_by=superuser_identity)
                instance.save()

    def create_methods(apps, schema_editor):
        superusers = User.objects.filter(is_superuser=True).all()
        superuser = superusers[0]
        superuser_identity = identity.models.Identity.objects.get(user_id=superuser.id)

        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        for method in methods:
            try:
                request_method = analytics.models.RequestMethod.objects.get(name=method)
            except Exception:
                request_method = analytics.models.RequestMethod(name=method, description='', created_by=superuser_identity)
                request_method.save()


    def create_ip_address_types(apps, schema_editor):
        superusers = User.objects.filter(is_superuser=True).all()
        superuser = superusers[0]
        superuser_identity = identity.models.Identity.objects.get(user_id=superuser.id)

        types = ['IPv4', 'IPv6', 'Invalid']
        for name in types:
            try:
                instance = analytics.models.IpAddressType.objects.get(name=name)
            except Exception:
                instance = analytics.models.IpAddressType(name=name, description='', created_by=superuser_identity)
                instance.save()


    def create_device_types(apps, schema_editor):
        superusers = User.objects.filter(is_superuser=True).all()
        superuser = superusers[0]
        superuser_identity = identity.models.Identity.objects.get(user_id=superuser.id)

        types = ['PC', 'Tablet', 'Mobile', 'Bot']
        for name in types:
            try:
                instance = analytics.models.DeviceType.objects.get(name=name)
            except Exception:
                instance = analytics.models.DeviceType(name=name, description='', created_by=superuser_identity)
                instance.save()


    operations = [
        migrations.RunPython(create_request_types),
        migrations.RunPython(create_methods),
        migrations.RunPython(create_ip_address_types),
        migrations.RunPython(create_device_types),
    ]
