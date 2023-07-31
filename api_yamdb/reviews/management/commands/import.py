import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Title
from users.models import User


class Command(BaseCommand):
    help = 'Фиктивное наполнение БД'

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--delete',
            action="store_true",
            help='Удаление записей из базы данных',
        )

    def _import_users(self):
        with open('static/data/users.csv') as f:
            reader = csv.DictReader(f)
            User.objects.bulk_create([User(**row) for row in reader])
        self.stdout.write('Пользователи успешно добавлены')

    def _import_categories(self):
        with open('static/data/category.csv') as f:
            reader = csv.DictReader(f)
            Category.objects.bulk_create([Category(**row) for row in reader])
        self.stdout.write('Категории успешно добавлены')

    def _import_titles(self):
        with open('static/data/titles.csv') as f:
            reader = csv.DictReader(f)
            Title.objects.bulk_create([Title(**row) for row in reader])
        self.stdout.write('Статьи успешно добавлены')

    def handle(self, *args, **options):
        if options['delete']:
            User.objects.all().delete()
            Category.objects.all().delete()
        else:
            self._import_users()
            self._import_categories()
            # self._import_titles()
