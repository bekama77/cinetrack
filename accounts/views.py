from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import RegisterForm, LoginForm, ProfileEditForm
from .models import Profile

class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("common:home")
    success_message = "Registration successful."

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"

class UserLogoutView(LogoutView):
    pass

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile_obj"

    def get_object(self, queryset=None):
        return self.request.user.profile

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"
    success_message = "Profile updated successfully."

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy("accounts:profile-detail")
