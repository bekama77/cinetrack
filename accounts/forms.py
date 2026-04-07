from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from .models import AppUser, Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))

    class Meta:
        model = AppUser
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio", "birth_date", "favorite_genres")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us about your movie taste"}),
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date and birth_date > timezone.localdate():
            raise forms.ValidationError("Birth date cannot be in the future.")
        return birth_date
