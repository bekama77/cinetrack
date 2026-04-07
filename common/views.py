from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import TemplateView

from movies.models import Movie
from reviews.models import Review


class HomePageView(TemplateView):
    template_name = "common/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_movies"] = Movie.objects.filter(is_public=True, is_featured=True).prefetch_related("genres")[:6]
        context["latest_reviews"] = Review.objects.filter(is_hidden=False).select_related("movie", "user")[:5]
        context["top_movies"] = (
            Movie.objects.filter(is_public=True)
            .annotate(avg_rating=Avg("reviews__rating"))
            .order_by("-avg_rating", "title")[:5]
        )
        return context


class AboutPageView(TemplateView):
    template_name = "common/about.html"


def custom_404(request, exception):
    return render(request, "common/404.html", status=404)


def custom_500(request):
    return render(request, "common/500.html", status=500)
