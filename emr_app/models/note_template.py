from django.db import models
from .provider_type import ProviderType

class NoteTemplate(models.Model):

    provide_type = models.ForeignKey(ProviderType, on_delete=models.DO_NOTHING)
    template = models.CharField()
