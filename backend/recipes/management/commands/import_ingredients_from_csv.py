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
            Ingredient.objects.bulk_create(
                Ingredient(**data) for data in reader
            )
        self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загружены.'))
