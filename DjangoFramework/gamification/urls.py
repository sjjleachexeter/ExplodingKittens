from django.urls import path

from gamification import views

urlpatterns = [
    path("", views.missions, name='missions'),
    path("quiz/<str:quiz_id>/", views.quiz, name='quiz'), #
    path("quiz/<str:quiz_id>/submit/", views.submit_answer, name='submit_answer'),
    path("start_mission/", views.start_mission, name='start_mission'),
    path("take_quiz/", views.take_quiz, name='take_quiz'),

    path("dashboard", views.dashboard, name='dashboard'),
    path("dashboard/edit_mission/<str:mission_id>", views.edit_mission, name='edit_mission'),
    path("dashboard/edit_mission/", views.edit_mission, name='create_mission'),
    path("dashboard/publish_mission/<str:mission_id>", views.publish_mission, name='publish_mission'),
    path("dashboard/edit_quiz/<str:quiz_id>", views.edit_quiz, name='edit_quiz'),
    path("dashboard/edit_quiz/", views.edit_quiz, name='create_quiz'),

]