import csv

from django.core.management.base import BaseCommand

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

    def handle(self, *args, **options):
        if options['delete']:
            User.objects.all().delete()
        else:
            self._import_users()
