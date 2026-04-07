from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from movies.models import Genre, Movie
from .models import WatchEntry, Collection

User = get_user_model()


class WatchlistTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", email="u1@example.com", password="pass12345")
        self.other = User.objects.create_user(username="u2", email="u2@example.com", password="pass12345")
        self.genre = Genre.objects.create(name="Sci-Fi")
        self.movie = Movie.objects.create(
            title="Movie A",
            description="Desc",
            release_year=2021,
            duration_minutes=100,
            created_by=self.user,
        )
        self.movie.genres.add(self.genre)

    def test_duplicate_watch_entry_not_allowed(self):
        WatchEntry.objects.create(user=self.user, movie=self.movie, status=WatchEntry.WANT)
        with self.assertRaises(Exception):
            WatchEntry.objects.create(user=self.user, movie=self.movie, status=WatchEntry.WATCHED, watched_at=timezone.localdate())

    def test_watched_entry_requires_date(self):
        entry = WatchEntry(user=self.user, movie=self.movie, status=WatchEntry.WATCHED)
        with self.assertRaises(ValidationError):
            entry.full_clean()

    def test_my_watchlist_requires_login(self):
        response = self.client.get(reverse("watchlists:my-watchlist"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_watch_entry(self):
        self.client.login(username="u1", password="pass12345")
        response = self.client.post(reverse("watchlists:watchentry-add"), data={
            "movie": self.movie.pk,
            "status": WatchEntry.WANT,
            "personal_note": "Need to watch",
            "is_favorite": True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WatchEntry.objects.filter(user=self.user, movie=self.movie).exists())

    def test_collection_detail_redirects_for_private_non_owner(self):
        collection = Collection.objects.create(owner=self.user, title="Private picks", is_public=False)
        response = self.client.get(reverse("watchlists:collection-detail", kwargs={"slug": collection.slug}))
        self.assertEqual(response.status_code, 302)

    def test_collection_owner_can_edit(self):
        collection = Collection.objects.create(owner=self.user, title="Owner picks", is_public=True)
        self.client.login(username="u1", password="pass12345")
        response = self.client.post(reverse("watchlists:collection-edit", kwargs={"slug": collection.slug}), data={
            "title": "Updated title",
            "description": "Updated",
            "is_public": True,
            "movies": [self.movie.pk],
        })
        self.assertEqual(response.status_code, 302)
        collection.refresh_from_db()
        self.assertEqual(collection.title, "Updated title")
