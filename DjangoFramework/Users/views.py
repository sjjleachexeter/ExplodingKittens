from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView


# Create your views here.
class AccountsView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "Users/accounts.html"

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("signup")
    template_name = "Users/signup.html"


