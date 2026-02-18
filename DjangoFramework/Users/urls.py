from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.AccountsView.as_view(), name="accounts"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("", include("django.contrib.auth.urls"), name="accounts"),
    path("delete_account/", views.delete_account, name="delete_account"),

]
