from django.contrib import admin
from .models import Genre, Movie

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "created_by", "is_public", "is_featured")
    list_filter = ("is_public", "is_featured", "genres")
    search_fields = ("title", "description")
    filter_horizontal = ("genres",)
