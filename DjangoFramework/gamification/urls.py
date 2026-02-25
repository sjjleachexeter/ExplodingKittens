from django.urls import path

from gamification import views

urlpatterns = [
    path("", views.missions, name='missions'),
    path("quiz/<str:quiz_id>", views.quiz, name='quiz'),
    path("start_mission", views.start_mission, name='start_mission'),
    path("take_quiz", views.take_quiz, name='take_quiz'),
]