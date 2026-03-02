from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    description = models.TextField()

class CustomUser(AbstractUser):
    roles = models.ManyToManyField(Role)

class Permission(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    code_name  = models.CharField(max_length=100, unique = True)

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)