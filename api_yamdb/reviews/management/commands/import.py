import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Title, Genre, Review, Comment
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
            Title.objects.bulk_create([Title(
                **{'category_id' if k == 'category' else k: v for k, v in
                   row.items()}) for row in reader])
        self.stdout.write('Статьи успешно добавлены')

    def _import_genres(self):
        with open('static/data/genre.csv') as f:
            reader = csv.DictReader(f)
            Genre.objects.bulk_create([Genre(**row) for row in reader])
        self.stdout.write('Жанры успешно добавлены')

    def _import_reviews(self):
        with open('static/data/review.csv') as f:
            reader = csv.DictReader(f)
            Review.objects.bulk_create([
                Review(**{'author_id' if k == 'author'
                          else k: v for k, v in row.items()})
                for row in reader])
        self.stdout.write('Отзывы успешно добавлены')

    def _import_comments(self):
        with open('static/data/comments.csv') as f:
            reader = csv.DictReader(f)
            Comment.objects.bulk_create([Comment(
                **{'author_id' if k == 'author'
                   else k: v for k, v in row.items()})
                for row in reader])
        self.stdout.write('Комментарии успешно добавлены')

    def _import_genre_to_title(self):
        with open('static/data/genre_title.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                genre = Genre.objects.get(pk=row['genre_id'])
                Title.objects.get(pk=row['title_id']).genre.add(genre)
        self.stdout.write('Жанры связаны с произведениями')

    def handle(self, *args, **options):
        if options['delete']:
            User.objects.all().delete()
            Category.objects.all().delete()
            Title.objects.all().delete()
            Genre.objects.all().delete()
            Review.objects.all().delete()
            Comment.objects.all().delete()
            self.stdout.write('База данных очищена')
        else:
            self._import_users()
            self._import_categories()
            self._import_titles()
            self._import_genres()
            self._import_reviews()
            self._import_comments()
            self._import_genre_to_title()
