from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="Scanner"),
    path("load_passport", views.load_passport, name="load_passport"),
    path("passporteditor/", views.manual_editor, name = "editor")
]
