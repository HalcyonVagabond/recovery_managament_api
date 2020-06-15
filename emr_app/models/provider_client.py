from django.db import models
from .client import Client
from .provider import Provider

class ProviderClient(models.Model):

    provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)