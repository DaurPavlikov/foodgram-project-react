from django.db.models import Manager


class RecipesRelatedManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'author'
        ).prefetch_related(
            'tags',
            'ingredients',
            'recipe',
            'shopping_cart',
            'favorite_recipe',
        )
