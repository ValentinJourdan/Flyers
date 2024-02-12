# Generated by Django 4.2.7 on 2023-11-22 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(default='', max_length=500)),
                ('event_type', models.CharField(choices=[('conference', 'Conférence'), ('workshop', 'Atelier'), ('meetup', 'Rencontre'), ('party', 'Soirée'), ('spectacle', 'Spectacle'), ('sport', 'Sport'), ('other', 'Autre')], default='other', max_length=20)),
                ('date', models.DateField(blank=True, null=True)),
                ('is_paid_event', models.BooleanField(default=False)),
                ('ticket_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, max_length=500, null=True, upload_to='', verbose_name='Illustration')),
                ('Roadmap', models.TextField(default='', null=True)),
                ('Likes', models.IntegerField(blank=True, default=0, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initiateur', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('money_man', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='money_man', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TinyCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tags', models.CharField(max_length=20)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart', to='Authentication.utilisateur')),
                ('event', models.ManyToManyField(blank=True, related_name='tags', to='Flow.event')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('tag', models.CharField(max_length=20)),
                ('nb_events', models.PositiveIntegerField(default=0)),
                ('event', models.ManyToManyField(related_name='tag', to='Flow.event')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_paid', models.BooleanField(default=False)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='Authentication.utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]