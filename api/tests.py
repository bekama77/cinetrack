from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from movies.models import Genre, Movie
from watchlists.models import WatchEntry

User = get_user_model()


class ApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", email="api@example.com", password="pass12345")
        self.genre = Genre.objects.create(name="Comedy")
        self.movie = Movie.objects.create(
            title="API Movie",
            description="Desc",
            release_year=2024,
            duration_minutes=95,
            created_by=self.user,
        )
        self.movie.genres.add(self.genre)

    def test_public_movie_api_returns_data(self):
        response = self.client.get(reverse("api:api-movie-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "API Movie")

    def test_watchlist_api_requires_authentication(self):
        response = self.client.get(reverse("api:api-watchentry-list-create"))
        self.assertEqual(response.status_code, 403)

    def test_authenticated_watchlist_api_lists_user_entries(self):
        WatchEntry.objects.create(user=self.user, movie=self.movie, status=WatchEntry.WANT)
        self.client.login(username="apiuser", password="pass12345")
        response = self.client.get(reverse("api:api-watchentry-list-create"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
