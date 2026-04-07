from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import MovieCreateForm, MovieEditForm
from .models import Movie

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().created_by == self.request.user

class MovieListView(ListView):
    model = Movie
    template_name = "movies/movie_list.html"
    context_object_name = "movies"
    paginate_by = 10

    def get_queryset(self):
        qs = Movie.objects.filter(is_public=True).prefetch_related("genres", "reviews")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return qs.distinct()

class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"

class MovieCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Movie
    form_class = MovieCreateForm
    template_name = "movies/movie_form.html"
    success_message = "Movie created successfully."

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("movies:movie-detail", kwargs={"slug": self.object.slug})

class MovieUpdateView(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Movie
    form_class = MovieEditForm
    template_name = "movies/movie_form.html"
    success_message = "Movie updated successfully."

    def get_success_url(self):
        return reverse_lazy("movies:movie-detail", kwargs={"slug": self.object.slug})

class MovieDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Movie
    template_name = "movies/movie_confirm_delete.html"
    success_url = reverse_lazy("movies:movie-list")
