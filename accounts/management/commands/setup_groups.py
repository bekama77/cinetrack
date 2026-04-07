from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.apps import apps

from movies.models import Movie, Genre
from reviews.models import Review


class Command(BaseCommand):
    help = "Create default Curators and Moderators groups with useful permissions."

    def handle(self, *args, **options):
        for app_config in apps.get_app_configs():
            create_permissions(app_config, verbosity=0)

        curators, _ = Group.objects.get_or_create(name="Curators")
        moderators, _ = Group.objects.get_or_create(name="Moderators")

        curator_permissions = Permission.objects.filter(
            content_type__in=[
                ContentType.objects.get_for_model(Movie),
                ContentType.objects.get_for_model(Genre),
            ]
        )
        moderator_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Review)
        )

        curators.permissions.set(curator_permissions)
        moderators.permissions.set(moderator_permissions)

        self.stdout.write(self.style.SUCCESS("Default groups created or updated successfully."))
