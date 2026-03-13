from django.contrib import admin
from django.contrib.auth.models import User

from Users.models import Level, Types


# Register your models here.
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass

@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    pass