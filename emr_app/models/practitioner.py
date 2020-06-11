from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class Practitioner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)