import csv
import os

from foodgram.settings import BASE_DIR
from base.models import Ingredient

path = os.path.join(BASE_DIR, 'data/')
os.chdir(path)

# Скрипт для испорта из файла CSV в базу данных Ingredient
with open('ingredients.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    Ingredient.objects.bulk_create(
        Ingredient(**row) for row in reader
    )
