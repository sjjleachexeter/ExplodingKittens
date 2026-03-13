from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from Users.decorators import superuser_required
from Users.models import Level, Types

from Leaderboard.models import LeaderboardPreferences


# Create your views here.
class AccountsView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    template_name = "Users/accounts.html"

    def get_context_data(self, **kwargs):
        # Get default context from the parent
        context = super().get_context_data(**kwargs)
        # add public setting
        if self.request.user.is_authenticated:
            try :
                public = self.request.user.leaderboard_preference

                context['public'] = public.public
            except LeaderboardPreferences.DoesNotExist:
                LeaderboardPreferences.objects.update_or_create(user=self.request.user)
                context['public'] = False

        return context


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
            Level.objects.update_or_create(user = authenticated_user)
            Types.objects.update_or_create(user = authenticated_user)
        else:
            print("Authentication failed after signup")
        return super().form_valid(form)


class LoginView(CreateView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("login")
    template_name = "registration/login.html"


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
    else:
        return redirect('delete_confirm')

@login_required
def logout_account(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    else:
        return redirect('logout_confirm')

@login_required
def public_account(request):
    if request.method == "POST":
        user = request.user
        preference = user.leaderboard_preference
        preference.toggle_public()
        preference.save()

        return redirect('accounts')
    else:
        return redirect('accounts')


class RoleForm(ModelForm):
    class Meta:
        model = Types
        fields = ['user','type']


@superuser_required
def edit_roles(request):
    if request.method == "POST":
        role_form = RoleForm(request.POST)

        if role_form.is_valid():
            role_form.save()

            # send user home on success
            return redirect('home')

    else:
        # create form to edit roles
        role_form = RoleForm()

    return render(request, "Users/edit_roles.html", {"role_form": role_form})