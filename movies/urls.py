from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, MovieDeleteView

app_name = "movies"
urlpatterns = [
    path("", MovieListView.as_view(), name="movie-list"),
    path("create/", MovieCreateView.as_view(), name="movie-create"),
    path("<slug:slug>/", MovieDetailView.as_view(), name="movie-detail"),
    path("<slug:slug>/edit/", MovieUpdateView.as_view(), name="movie-edit"),
    path("<slug:slug>/delete/", MovieDeleteView.as_view(), name="movie-delete"),
]
