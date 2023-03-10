import csv
from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из csv файла'

    def handle(self, *args, **kwargs):
        path = Path(settings.BASE_DIR, 'data', 'ingredients.csv').resolve()
        with open(path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                db = Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
                db.save()
        self.stdout.write(self.style.SUCCESS(
            'Ингредиенты из json-файла успешно загружены.'
        ))
