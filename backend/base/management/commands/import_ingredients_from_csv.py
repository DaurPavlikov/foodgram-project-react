import csv
import os

from django.conf import settings
from django.core.management import BaseCommand
from base.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из csv файла'

    def handle(self, *args, **kwargs):
        path = os.path.join(settings.BASE_DIR, 'static/data/')
        os.chdir(path)
        with open('ingredients.csv', mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                db = Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                db.save()
        self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загружены.'))
