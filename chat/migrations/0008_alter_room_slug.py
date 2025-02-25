# Generated by Django 5.1.6 on 2025-02-25 18:22

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_room_last_message_alter_room_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.SlugField(default=shortuuid.main.ShortUUID.uuid, editable=False, unique=True),
        ),
    ]
