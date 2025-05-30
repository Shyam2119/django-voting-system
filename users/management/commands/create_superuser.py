from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'shyam')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'shyampattipu@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'shyam@123')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists!')
            )