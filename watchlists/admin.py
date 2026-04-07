from django.contrib import admin
from .models import WatchEntry, Collection

@admin.register(WatchEntry)
class WatchEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "status", "is_favorite", "watched_at")
    list_filter = ("status", "is_favorite")

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_public")
    list_filter = ("is_public",)
    filter_horizontal = ("movies",)
