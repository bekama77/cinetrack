from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    trailer_url = models.URLField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="movies")
    genres = models.ManyToManyField(Genre, related_name="movies")
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("title", "release_year")

    def clean(self):
        if self.release_year < 1888 or self.release_year > timezone.now().year:
            raise ValidationError({"release_year": "Enter a valid release year."})
        if self.duration_minutes <= 0:
            raise ValidationError({"duration_minutes": "Duration must be greater than 0."})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.release_year}")
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.release_year})"
