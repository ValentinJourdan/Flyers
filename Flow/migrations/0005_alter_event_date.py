# Generated by Django 4.2.7 on 2023-11-22 20:24

import Flow.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flow', '0004_event_max_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(blank=True, default=Flow.models.default_event_date),
        ),
    ]