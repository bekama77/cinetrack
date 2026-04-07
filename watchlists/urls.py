from django.urls import path
from .views import (
    MyWatchlistView,
    DashboardView,
    RecommendationListView,
    WatchEntryCreateView,
    WatchEntryUpdateView,
    WatchEntryDeleteView,
    CollectionListView,
    CollectionDetailView,
    CollectionCreateView,
    CollectionUpdateView,
    CollectionDeleteView,
)

app_name = "watchlists"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("recommendations/", RecommendationListView.as_view(), name="recommendations"),
    path("mine/", MyWatchlistView.as_view(), name="my-watchlist"),
    path("entry/add/", WatchEntryCreateView.as_view(), name="watchentry-add"),
    path("entry/<int:pk>/edit/", WatchEntryUpdateView.as_view(), name="watchentry-edit"),
    path("entry/<int:pk>/delete/", WatchEntryDeleteView.as_view(), name="watchentry-delete"),
    path("collections/", CollectionListView.as_view(), name="collection-list"),
    path("collections/create/", CollectionCreateView.as_view(), name="collection-create"),
    path("collections/<slug:slug>/", CollectionDetailView.as_view(), name="collection-detail"),
    path("collections/<slug:slug>/edit/", CollectionUpdateView.as_view(), name="collection-edit"),
    path("collections/<slug:slug>/delete/", CollectionDeleteView.as_view(), name="collection-delete"),
]
