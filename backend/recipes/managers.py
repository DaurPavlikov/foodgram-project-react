from django.db import models


class RecipesRelatedManager(models.Manager):
    """Менеджер для получения списка рецептов со всеми связанными моделями."""

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author'
        ).prefetch_related(
            'tags',
            'ingredients',
            'foreign_recipes',
            'shopping_cart',
            'favorite_recipe',
        )
