import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class LeaderboardPreferences(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name = "leaderboard_preference")
    public = models.BooleanField(default = False)

    def toggle_public(self):
        self.public = not self.public

