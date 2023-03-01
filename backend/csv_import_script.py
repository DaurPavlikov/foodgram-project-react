import csv
import os

from foodgram.settings import BASE_DIR
from base.models import Ingredient

path = os.path.join(BASE_DIR, 'static/data/')
os.chdir(path)

# Скрипт для испорта из файла CSV в базу данных Ingredient
with open('users.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Ingredient(
            name=row['name'],
            measurement_unit=row['measurement_unit'],
        )
        db.save()
