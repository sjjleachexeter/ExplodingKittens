from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView


# Create your views here.
class AccountsView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "Users/accounts.html"


class SignupView(FormView):
    template_name = "Users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        authenticated_user = authenticate(
            self.request,
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password1")
        )
        if authenticated_user is not None:
            login(self.request, authenticated_user)
            print(f"User logged in: {self.request.user}")
        else:
            print("Authentication failed after signup")
        return super().form_valid(form)

class LoginView(CreateView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("login")
    template_name = "registration/login.html"

