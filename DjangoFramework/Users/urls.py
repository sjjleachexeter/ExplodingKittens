from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.AccountsView.as_view(), name="accounts"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("", include("django.contrib.auth.urls"), name="accounts"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("logout_account/", views.logout_account, name="logout_account"),
    path("public_account", views.public_account, name="public_account"),
]
