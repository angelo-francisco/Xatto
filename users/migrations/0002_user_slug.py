# Generated by Django 5.1.6 on 2025-02-19 04:04

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True),
        ),
    ]
