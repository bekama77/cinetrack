from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from movies.models import Genre, Movie
from .models import Review

User = get_user_model()


class ReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", email="reviewer@example.com", password="pass12345")
        self.genre = Genre.objects.create(name="Thriller")
        self.movie = Movie.objects.create(
            title="Review Movie",
            description="Desc",
            release_year=2022,
            duration_minutes=110,
            created_by=self.user,
        )
        self.movie.genres.add(self.genre)

    def test_invalid_rating_raises(self):
        review = Review(user=self.user, movie=self.movie, title="Bad", content="Bad", rating=9)
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_authenticated_user_can_create_review(self):
        self.client.login(username="reviewer", password="pass12345")
        response = self.client.post(reverse("reviews:review-create"), data={
            "movie": self.movie.pk,
            "title": "Great",
            "content": "Really enjoyed it.",
            "rating": 5,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(movie=self.movie, user=self.user).exists())

    def test_review_list_view_returns_200(self):
        Review.objects.create(user=self.user, movie=self.movie, title="Great", content="Text", rating=5)
        response = self.client.get(reverse("reviews:review-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Great")

    def test_only_owner_can_edit_review(self):
        review = Review.objects.create(user=self.user, movie=self.movie, title="Great", content="Text", rating=5)
        other = User.objects.create_user(username="other", email="other@example.com", password="pass12345")
        self.client.login(username="other", password="pass12345")
        response = self.client.get(reverse("reviews:review-edit", kwargs={"pk": review.pk}))
        self.assertEqual(response.status_code, 403)
