# Generated by Django 5.1.6 on 2025-02-19 04:04

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_room_slug_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.SlugField(default=shortuuid.main.ShortUUID.uuid, editable=False, unique=True),
        ),
    ]
