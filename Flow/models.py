from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Authentication.models import Utilisateur
from datetime import timedelta

def default_event_date():
    return timezone.now() + timedelta(days=2)


class Event(models.Model):
    EVENT_TYPES = [
        	('conference', 'Conférence'),
            ('workshop', 'Atelier'),
            ('meetup', 'Rencontre'),
            ('party', 'Soirée'),
            ('spectacle', 'Spectacle'),
            ('sport', 'Sport'),
            ('other', 'Autre')
    ]

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default='')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other',null=True)
    date = models.DateField(default=default_event_date, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiateur', null=True)
    is_paid_event = models.BooleanField(default=False)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    money_man = models.ForeignKey(User, on_delete=models.CASCADE, related_name='money_man', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event/', null=True, blank=True, default="event/default.jpg")
    members = models.ManyToManyField(User, blank=True)
    max_members = models.PositiveIntegerField(default=10)
    Roadmap = models.TextField(default='', null=True)
    Likes = models.IntegerField(default=0, blank=True, null=True)

class Like(models.Model):
    event_id = models.IntegerField(default=0, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Tags(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    tag = models.CharField(max_length=20, default='')
    event = models.ManyToManyField(Event, related_name='tag')
    nb_events = models.PositiveIntegerField(default=0)

