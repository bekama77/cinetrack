from django.urls import path
from .views import MovieListAPIView, MovieDetailAPIView, ReviewListAPIView, MyWatchEntryListCreateAPIView, MyWatchEntryDetailAPIView

app_name = "api"
urlpatterns = [
    path("movies/", MovieListAPIView.as_view(), name="api-movie-list"),
    path("movies/<slug:slug>/", MovieDetailAPIView.as_view(), name="api-movie-detail"),
    path("reviews/", ReviewListAPIView.as_view(), name="api-review-list"),
    path("watchlist/", MyWatchEntryListCreateAPIView.as_view(), name="api-watchentry-list-create"),
    path("watchlist/<int:pk>/", MyWatchEntryDetailAPIView.as_view(), name="api-watchentry-detail"),
]
