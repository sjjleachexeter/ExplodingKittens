from django.urls import path
from . import views

urlpatterns = [
    # Basic navigation
    path("", views.home, name='home'),
    path("scan/", views.scan, name='scan'),
    path("product/", views.product_passport, name='product'),
    path("missions/", views.missions, name='missions'),
    path("leaderboard/", views.leaderboard, name='leaderboard'),
    path("profile/", views.profile, name='profile'),
    path("user/", views.user, name='user'),
    path("signup/", views.signup, name='signup'),
    path("login/", views.login, name='login'),


    # GDPR compliance
    path("privacy/", views.privacy, name='privacy'),
    path("terms-and-conditions/", views.terms, name='terms'),
    path("about/", views.about, name='about')
]