from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class User(AbstractBaseUser):
    class Types(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        GAMES_ADMIN = "GAMES_ADMIN", "Games_admin"
        PASSPORT_ADMIN = "PASSPORT_ADMIN", "Passport_admin"
        GEN_USER = "GEN_USER", "Gen_user"

    type = models.CharField(max_length=20, choices = Types.choices, default = Types.MANAGER)

    def __str__(self):
        return self.email
