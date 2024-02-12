
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Utilisateur(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='utilisateur')
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    joined_nb = models.PositiveIntegerField(default=0)
    created_nb = models.PositiveIntegerField(default=0)
    CA_buys = models.FloatField(default=0)
    is_validated_money_man = models.BooleanField(default=False)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)
    CA_sales = models.FloatField(default=0)
    avatar = models.ImageField(
        upload_to='avatar/', null=True, blank=True, default="avatar/default.jpg")
    money_man_request_pending = models.BooleanField(default=False)
