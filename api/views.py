from rest_framework import generics, permissions
from movies.models import Movie
from reviews.models import Review
from watchlists.models import WatchEntry

from .permissions import IsOwnerOfWatchEntry
from .serializers import MovieSerializer, ReviewSerializer, WatchEntrySerializer

class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.filter(is_public=True).prefetch_related("genres")
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.filter(is_public=True).prefetch_related("genres")
    serializer_class = MovieSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.filter(is_hidden=False).select_related("movie", "user")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

class MyWatchEntryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = WatchEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchEntry.objects.filter(user=self.request.user).select_related("movie")

class MyWatchEntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WatchEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfWatchEntry]

    def get_queryset(self):
        return WatchEntry.objects.filter(user=self.request.user)
