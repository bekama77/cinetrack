from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from movies.models import Genre

User = get_user_model()


class AccountTests(TestCase):
    def test_register_creates_user_and_profile(self):
        response = self.client.post(reverse("accounts:register"), data={
            "username": "john",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "VeryStrongPass123",
            "password2": "VeryStrongPass123",
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="john")
        self.assertTrue(hasattr(user, "profile"))

    def test_login_works(self):
        User.objects.create_user(username="john", email="john@example.com", password="pass12345")
        response = self.client.post(reverse("accounts:login"), data={
            "username": "john",
            "password": "pass12345",
        })
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_requires_login(self):
        response = self.client.get(reverse("accounts:profile-edit"))
        self.assertEqual(response.status_code, 302)

    def test_profile_update_changes_bio(self):
        user = User.objects.create_user(username="john", email="john@example.com", password="pass12345")
        genre = Genre.objects.create(name="Drama")
        self.client.login(username="john", password="pass12345")
        response = self.client.post(reverse("accounts:profile-edit"), data={
            "bio": "Loves sci-fi and thrillers",
            "favorite_genres": [genre.pk],
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.profile.bio, "Loves sci-fi and thrillers")
