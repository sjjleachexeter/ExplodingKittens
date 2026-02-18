from django.urls import path

from gamification import views

urlpatterns = [
    path("", views.missions, name='missions'),
    path("quiz/<str:quiz_id>", views.quiz, name='quiz'),
]