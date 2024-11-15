"""Команда загрузки CSV файлов в БД: python manage.py load_csv."""
import csv

from django.conf import settings
from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import (CustomUser,
                            Title,
                            Category,
                            Genre,
                            Review,
                            Comment
                            )


MODELS_CSVFILES = {CustomUser: 'users.csv',
                   Category: 'category.csv',
                   Genre: 'genre.csv',
                   Title: 'titles.csv',
                   Review: 'review.csv',
                   Comment: 'comments.csv'}


class Command(BaseCommand):
    """Класс загрузки CSV файлов в БД."""

    def handle(self, *args, **kwargs):
        for model, csv_file in MODELS_CSVFILES.items():
            try:
                with open(f'{settings.STATICFILES_DIRS[0]}/data/{csv_file}',
                          'r', encoding='utf-8') as file:
                    rows = csv.DictReader(file)
                    model.objects.bulk_create(model(**row) for row in rows)
                    self.stdout.write(self.style.SUCCESS(
                        f'Данные модели {model.__name__} загружены'))
            except IntegrityError as error:
                self.stdout.write(self.style.ERROR(
                    f'Ошибка загрузки модели {model.__name__} - {error}'))
            except Exception as error:
                self.stdout.write(self.style.ERROR(f'Ошибка {error}'))
        try:
            with open('static/data/genre_title.csv', 'r') as csv_file:
                rows = csv.DictReader(csv_file)
                for row in rows:
                    Title(pk=row['title_id']).genre.add(
                        Genre(pk=row['genre_id']))
                self.stdout.write(self.style.SUCCESS(
                    'Данные модели TitleGenre загружены'))
        except Exception as error:
            self.stdout.write(self.style.ERROR(f'Ошибка {error}'))
