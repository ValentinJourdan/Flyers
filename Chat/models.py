from django.db import models

from Authentication.models import User
from Flow.models import Event


class Message(models.Model):
    body = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('created_at',)

        def __str__(self):
            return f'{self.sent_by}'


class Room(models.Model):
    ACTIVE = 'active'
    CLOSED = 'closed'
    CHOICES_STATUS = (
        (CLOSED, 'closed'),
        (ACTIVE, 'active'),

    )
    eId = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=True, null=True)
    messages = models.ManyToManyField(Message, blank=True)
    # url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=CHOICES_STATUS, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, related_name='room', null=True)

    class Meta:
        ordering = ('-created_at',)

        def __str__(self):
            return f'{self.uuid}'


class Sondage(models.Model):
    question = models.CharField(max_length=200)


class Reponse(models.Model):
    sondage = models.ForeignKey(
        Sondage, related_name='reponses', on_delete=models.CASCADE)
    choix = models.CharField(max_length=100)
    # Autres champs pour enregistrer les réponses
