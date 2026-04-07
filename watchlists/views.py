from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from movies.models import Movie
from .forms import WatchEntryForm, CollectionCreateForm, CollectionEditForm
from .models import WatchEntry, Collection


class CollectionOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().owner == self.request.user


class MyWatchlistView(LoginRequiredMixin, ListView):
    model = WatchEntry
    template_name = "watchlists/my_watchlist.html"
    context_object_name = "entries"

    def get_queryset(self):
        status = self.request.GET.get("status")
        queryset = WatchEntry.objects.filter(user=self.request.user).select_related("movie")
        if status in {WatchEntry.WANT, WatchEntry.WATCHING, WatchEntry.WATCHED}:
            queryset = queryset.filter(status=status)
        return queryset


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "watchlists/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = WatchEntry.objects.filter(user=self.request.user)
        context["total_entries"] = entries.count()
        context["watched_count"] = entries.filter(status=WatchEntry.WATCHED).count()
        context["watching_count"] = entries.filter(status=WatchEntry.WATCHING).count()
        context["want_count"] = entries.filter(status=WatchEntry.WANT).count()
        context["favorite_entries"] = entries.filter(is_favorite=True).select_related("movie")[:5]
        context["collections_count"] = self.request.user.collections.count()
        return context


class RecommendationListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = "watchlists/recommendations.html"
    context_object_name = "movies"

    def get_queryset(self):
        favorite_genres = self.request.user.profile.favorite_genres.all()
        watched_movie_ids = self.request.user.watch_entries.values_list("movie_id", flat=True)
        queryset = Movie.objects.filter(is_public=True).exclude(id__in=watched_movie_ids)
        if favorite_genres.exists():
            queryset = queryset.filter(genres__in=favorite_genres)
        return queryset.prefetch_related("genres").distinct()[:12]


class WatchEntryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = WatchEntry
    form_class = WatchEntryForm
    template_name = "watchlists/watchentry_form.html"
    success_url = reverse_lazy("watchlists:my-watchlist")
    success_message = "Movie added to your watchlist."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_movie_ids = self.request.user.watch_entries.values_list("movie_id", flat=True)
        form.fields["movie"].queryset = Movie.objects.filter(is_public=True).exclude(id__in=user_movie_ids)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WatchEntryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = WatchEntry
    form_class = WatchEntryForm
    template_name = "watchlists/watchentry_form.html"
    success_url = reverse_lazy("watchlists:my-watchlist")
    success_message = "Watch entry updated."

    def get_queryset(self):
        return WatchEntry.objects.filter(user=self.request.user)


class WatchEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = WatchEntry
    success_url = reverse_lazy("watchlists:my-watchlist")
    template_name = "watchlists/watchentry_confirm_delete.html"

    def get_queryset(self):
        return WatchEntry.objects.filter(user=self.request.user)


class CollectionListView(ListView):
    model = Collection
    template_name = "watchlists/collection_list.html"
    context_object_name = "collections"

    def get_queryset(self):
        queryset = Collection.objects.filter(is_public=True).prefetch_related("movies", "owner")
        if self.request.user.is_authenticated:
            queryset = Collection.objects.filter(Q(is_public=True) | Q(owner=self.request.user)).distinct().prefetch_related("movies", "owner")
        return queryset


class CollectionDetailView(DetailView):
    model = Collection
    template_name = "watchlists/collection_detail.html"
    context_object_name = "collection"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.is_public and obj.owner != request.user:
            return redirect("watchlists:collection-list")
        return super().dispatch(request, *args, **kwargs)


class CollectionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Collection
    form_class = CollectionCreateForm
    template_name = "watchlists/collection_form.html"
    success_message = "Collection created."

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("watchlists:collection-detail", kwargs={"slug": self.object.slug})


class CollectionUpdateView(LoginRequiredMixin, CollectionOwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Collection
    form_class = CollectionEditForm
    template_name = "watchlists/collection_form.html"
    success_message = "Collection updated."

    def get_success_url(self):
        return reverse_lazy("watchlists:collection-detail", kwargs={"slug": self.object.slug})


class CollectionDeleteView(LoginRequiredMixin, CollectionOwnerRequiredMixin, DeleteView):
    model = Collection
    template_name = "watchlists/collection_confirm_delete.html"
    success_url = reverse_lazy("watchlists:collection-list")
