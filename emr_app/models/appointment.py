from django.db import models
from .client import Client
from .provider import Provider

class Appointment(models.Model):

    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    duration = models.IntegerField(default=30)
    virtual_boolean = models.BooleanField(default=True)
    appointment_url = models.URLField(max_length=200, null=True)