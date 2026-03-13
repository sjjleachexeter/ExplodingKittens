import uuid
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class Level(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name = "current_level")
    level = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return str(f"{self.user} - Level {self.level}")
# request.user.current_level.level

class Types(models.Model):
    class Roles(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        GAMES_ADMIN = "GAMES_ADMIN", "Games_admin"
        PASSPORT_ADMIN = "PASSPORT_ADMIN", "Passport_admin"
        GEN_USER = "GEN_USER", "Gen_user"

    type = models.CharField(max_length=20, choices = Roles.choices, default = Roles.GEN_USER)
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name = "role")
    def __str__(self):
        return str(f"{self.user} - {self.type}")
# request.user.role.type
