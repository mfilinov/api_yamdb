import csv

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Фиктивное наполнение БД'

    def handle(self, *args, **options):
        with open('static/data/users.csv') as f:
            reader = csv.DictReader(f)
            User.objects.bulk_create([User(**row) for row in reader])
        self.stdout.write('Пользователи успешно добавлены')
