from django import template
from django.db.models import Avg

register = template.Library()

@register.filter
def stars_from_rating(value):
    try:
        value = int(round(float(value)))
    except (TypeError, ValueError):
        return ""
    return "★" * value + "☆" * (5 - value)

@register.simple_tag
def average_movie_rating(movie):
    avg = movie.reviews.filter(is_hidden=False).aggregate(avg=Avg("rating"))["avg"]
    return round(avg, 1) if avg else "No ratings"

@register.simple_tag
def user_watched_count(user):
    return user.watch_entries.filter(status="watched").count() if user.is_authenticated else 0
