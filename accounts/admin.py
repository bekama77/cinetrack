from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser, Profile

@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ("username", "email", "is_staff", "is_active")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "birth_date")
    filter_horizontal = ("favorite_genres",)
