from django.urls import path

from Leaderboard import views

urlpatterns = [
    path("", views.leaderboard, name='leaderboard'),
]