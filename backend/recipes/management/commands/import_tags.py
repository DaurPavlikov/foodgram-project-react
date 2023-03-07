from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Импорт тегов'

    def handle(self, *args, **kwargs):
        data = [
            {'id': 3, 'name': 'Пустота', 'color': '#FFFFFF', 'slug': 'all_empty'},
            {'id': 2, 'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'breakfast'},
            {'id': 1, 'name': 'Обед', 'color': '#49B64E', 'slug': 'dinner'},
            {'id': 0, 'name': 'Ужин', 'color': '#8775D2', 'slug': 'supper'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Тэги успешно импортированы.'))
