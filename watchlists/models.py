from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from movies.models import Movie

class WatchEntry(models.Model):
    WANT = "want_to_watch"
    WATCHING = "watching"
    WATCHED = "watched"
    STATUS_CHOICES = [(WANT, "Want to watch"), (WATCHING, "Watching"), (WATCHED, "Watched")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watch_entries")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watch_entries")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=WANT)
    added_at = models.DateTimeField(auto_now_add=True)
    watched_at = models.DateField(blank=True, null=True)
    personal_note = models.TextField(blank=True)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "movie")
        ordering = ("-added_at",)

    def clean(self):
        if self.watched_at and self.watched_at > timezone.localdate():
            raise ValidationError({"watched_at": "Watched date cannot be in the future."})
        if self.status == self.WATCHED and not self.watched_at:
            raise ValidationError({"watched_at": "Provide a watched date for watched movies."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Collection(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="collections")
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    movies = models.ManyToManyField(Movie, blank=True, related_name="collections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("owner", "title")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.owner.username}-{self.title}")
        super().save(*args, **kwargs)
