from rest_framework import serializers
from movies.models import Movie
from reviews.models import Review
from watchlists.models import WatchEntry

class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Movie
        fields = ("id", "title", "slug", "description", "release_year", "duration_minutes", "trailer_url", "genres", "created_by", "is_featured")

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    movie = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ("id", "movie", "user", "title", "content", "rating", "created_at")

class WatchEntrySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WatchEntry
        fields = ("id", "user", "movie", "status", "watched_at", "personal_note", "is_favorite")
