from django.contrib import admin

from gamification.models import Mission, MissionProgress, Quiz, QuizAttempt
from passport.models import Ingredient


# Register your models here.
@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    pass


@admin.register(MissionProgress)
class MissionProgressAdmin(admin.ModelAdmin):
    pass


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    pass