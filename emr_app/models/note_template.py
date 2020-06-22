from django.db import models
from .provider_type import ProviderType

class NoteTemplate(models.Model):

    template = models.TextField()
