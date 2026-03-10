from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="Scanner"),
    path("passporteditor/", views.manual_editor, name = "editor")
]