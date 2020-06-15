from django.db import models
from .note_template import NoteTemplate
from .client import Client
from .provider import Provider

class Note(models.Model):

    note_template = models.ForeignKey(NoteTemplate, on_delete=models.DO_NOTHING)
    content = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField(auto_now_add=True)