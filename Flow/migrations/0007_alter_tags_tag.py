# Generated by Django 4.2.7 on 2023-11-22 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flow', '0006_remove_tinycart_client_remove_tinycart_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='tag',
            field=models.CharField(default='', max_length=20),
        ),
    ]