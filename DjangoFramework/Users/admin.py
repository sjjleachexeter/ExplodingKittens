from django.contrib import admin
from django.contrib.auth.models import User

from Users.models import Level


# Register your models here.
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass