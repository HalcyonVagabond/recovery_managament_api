from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .provider_type import ProviderType


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=55)
    practice_name = models.CharField(max_length=255)
    practice_address = models.CharField(max_length=255)
    provider_type = models.ForeignKey(ProviderType, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = (F('id').asc(nulls_last=True),)