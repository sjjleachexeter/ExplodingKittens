import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Level(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name = "current_level")
    level = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
