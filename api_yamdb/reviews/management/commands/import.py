import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Title, Genre, Comment, Review
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
        fieldnames = ('id', 'name', 'slug')
        with open('static/data/category.csv', encoding="utf8") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = fieldnames
            next(reader)
            Category.objects.bulk_create([Category(**row) for row in reader])
        self.stdout.write('Категории успешно добавлены')

    def _import_titles(self):
        fieldnames = ('id', 'name', 'year', 'category_id')
        with open('static/data/titles.csv', encoding="utf8") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = fieldnames
            next(reader)
            Title.objects.bulk_create([Title(**row) for row in reader])
        self.stdout.write('Статьи успешно добавлены')

    def _import_genres(self):
        fieldnames = ('id', 'name', 'slug')
        with open('static/data/genre.csv', encoding="utf8") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = fieldnames
            next(reader)
            Genre.objects.bulk_create([Genre(**row) for row in reader])
        self.stdout.write('Жанры успешно добавлены')

    def _import_reviews(self):
        fieldnames = ('id', 'title_id', 'text',
                      'author_id', 'score', 'pub_date')
        with open('static/data/review.csv', encoding="utf8") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = fieldnames
            next(reader)
            Review.objects.bulk_create([Review(**row) for row in reader])
        self.stdout.write('Отзывы успешно добавлены')

    def _import_comments(self):
        fieldnames = ('id', 'review_id', 'text', 'author_id', 'pub_date')
        with open('static/data/comments.csv', encoding="utf8") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = fieldnames
            next(reader)
            Comment.objects.bulk_create([Comment(**row) for row in reader])
        self.stdout.write('Комментарии успешно добавлены')

    def _import_relationships(self):
        fieldnames = ('id', 'title_id', 'genre_id')
        with open('static/data/genre_title.csv', encoding="utf8") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = fieldnames
            next(reader)
            for row in reader:
                Title.objects.get(
                    pk=row['title_id']).genre.add(
                    Genre.objects.get(pk=row['genre_id']))
        self.stdout.write('Жанры связаны с произведениями')

    def handle(self, *args, **options):
        if options['delete']:
            User.objects.all().delete()
            Category.objects.all().delete()
        else:
            self._import_users()
            self._import_categories()
            self._import_titles()
            self._import_genres()
            self._import_reviews()
            self._import_comments()
            self._import_relationships()
