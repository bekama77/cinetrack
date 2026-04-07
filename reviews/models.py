from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from movies.models import Movie

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField()
    is_hidden = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("user", "movie")

    def clean(self):
        if not 1 <= self.rating <= 5:
            raise ValidationError({"rating": "Rating must be between 1 and 5."})

    def save(self, *args, **kwargs):
        if self.pk:
            self.is_edited = True
        self.full_clean()
        super().save(*args, **kwargs)
