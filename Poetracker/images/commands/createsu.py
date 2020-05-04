from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="riley").exists():
            User.objects.create_superuser("riley", "admin@admin.com", "crinkle1311")
