from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from movies.models import Genre, Movie
from reviews.models import Review
from watchlists.models import Collection, WatchEntry

User = get_user_model()

GENRES = ["Action", "Drama", "Sci-Fi", "Thriller", "Comedy"]
MOVIES = [
    ("Interstellar", 2014, "A team travels through a wormhole to save humanity.", 169, ["Sci-Fi", "Drama"]),
    ("Inception", 2010, "A skilled thief enters dreams to steal secrets.", 148, ["Sci-Fi", "Thriller"]),
    ("The Dark Knight", 2008, "Batman faces the Joker in Gotham City.", 152, ["Action", "Drama"]),
    ("Parasite", 2019, "A poor family infiltrates a wealthy household.", 132, ["Drama", "Thriller"]),
    ("Whiplash", 2014, "A jazz student pushes himself to the limit.", 106, ["Drama"]),
    ("Arrival", 2016, "A linguist communicates with alien visitors.", 116, ["Sci-Fi", "Drama"]),
]


class Command(BaseCommand):
    help = "Seed demo genres, movies, reviews, collections and watchlist entries."

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            username="demo_user",
            defaults={"email": "demo@example.com", "first_name": "Demo", "last_name": "User"},
        )
        if not user.has_usable_password():
            user.set_password("demo12345")
            user.save()

        genre_map = {}
        for name in GENRES:
            genre, _ = Genre.objects.get_or_create(name=name)
            genre_map[name] = genre

        user.profile.favorite_genres.set([genre_map["Sci-Fi"], genre_map["Drama"]])

        created_movies = []
        for title, year, description, duration, genre_names in MOVIES:
            movie, _ = Movie.objects.get_or_create(
                title=title,
                release_year=year,
                defaults={
                    "description": description,
                    "duration_minutes": duration,
                    "created_by": user,
                    "is_featured": True,
                    "is_public": True,
                },
            )
            movie.genres.set([genre_map[name] for name in genre_names])
            created_movies.append(movie)

        for index, movie in enumerate(created_movies[:3], start=1):
            Review.objects.get_or_create(
                user=user,
                movie=movie,
                defaults={
                    "title": f"Thoughts on {movie.title}",
                    "content": f"Sample review #{index} for {movie.title}.",
                    "rating": 4 if index < 3 else 5,
                },
            )

        collection, _ = Collection.objects.get_or_create(
            owner=user,
            title="Weekend Essentials",
            defaults={"description": "A small public starter collection.", "is_public": True},
        )
        collection.movies.set(created_movies[:4])

        for movie in created_movies[:4]:
            WatchEntry.objects.get_or_create(
                user=user,
                movie=movie,
                defaults={"status": WatchEntry.WATCHED if movie.title != "Arrival" else WatchEntry.WANT, "watched_at": __import__("django.utils.timezone").utils.timezone.localdate() if movie.title != "Arrival" else None},
            )

        self.stdout.write(self.style.SUCCESS("Demo data created. Login with demo_user / demo12345"))
