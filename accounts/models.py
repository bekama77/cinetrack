from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models

class AppUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, validators=[MaxLengthValidator(400)])
    birth_date = models.DateField(blank=True, null=True)
    favorite_genres = models.ManyToManyField("movies.Genre", blank=True, related_name="fans")

    def __str__(self):
        return f"{self.user.username}'s profile"
