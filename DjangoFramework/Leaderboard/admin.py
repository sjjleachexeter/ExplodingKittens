from django.contrib import admin

from Leaderboard.models import LeaderboardPreferences


# Register your models here.
@admin.register(LeaderboardPreferences)
class LeaderboardPreferencesAdmin(admin.ModelAdmin):
    pass