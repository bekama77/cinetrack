from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from movies.models import Movie

User = get_user_model()

@shared_task
def send_weekly_recommendations():
    users = User.objects.select_related("profile").prefetch_related("profile__favorite_genres")
    sent_count = 0
    for user in users:
        favorite_genres = user.profile.favorite_genres.all()
        if not favorite_genres.exists() or not user.email:
            continue
        recommendations = Movie.objects.filter(is_public=True, genres__in=favorite_genres).distinct()[:5]
        if not recommendations:
            continue
        movie_lines = "\n".join([f"- {movie.title} ({movie.release_year})" for movie in recommendations])
        send_mail(
            subject="Your CineTrack weekly recommendations",
            message=f"Hi {user.username},\n\nHere are a few movies for you:\n{movie_lines}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        sent_count += 1
    return sent_count
