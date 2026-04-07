from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Movie, Genre

User = get_user_model()


class MovieModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="tester@example.com", password="pass12345")
        self.genre = Genre.objects.create(name="Drama")

    def test_movie_invalid_release_year_raises(self):
        movie = Movie(
            title="Bad Year",
            description="Test",
            release_year=1700,
            duration_minutes=100,
            created_by=self.user,
        )
        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_movie_slug_is_created(self):
        movie = Movie.objects.create(
            title="Test Movie",
            description="Test description",
            release_year=2020,
            duration_minutes=120,
            created_by=self.user,
        )
        movie.genres.add(self.genre)
        self.assertTrue(movie.slug.startswith("test-movie-2020"))

    def test_movie_list_view_returns_200(self):
        movie = Movie.objects.create(
            title="Public Movie",
            description="Test description",
            release_year=2020,
            duration_minutes=120,
            created_by=self.user,
        )
        movie.genres.add(self.genre)
        response = self.client.get(reverse("movies:movie-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Public Movie")

    def test_authenticated_user_can_create_movie(self):
        self.client.login(username="tester", password="pass12345")
        response = self.client.post(reverse("movies:movie-create"), data={
            "title": "Arrival",
            "description": "Aliens arrive.",
            "release_year": 2016,
            "duration_minutes": 116,
            "trailer_url": "",
            "genres": [self.genre.pk],
            "is_featured": True,
            "is_public": True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Movie.objects.filter(title="Arrival").exists())
