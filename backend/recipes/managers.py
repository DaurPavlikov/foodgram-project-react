from django.db import models


class RecipesRelatedManager(models.Manager):
    """Менеджер для получения списка рецептов со всеми связанными моделями."""

    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug__in=self.request.query_params.getlist('tags')
        ).distinct().select_related(
            'author'
        ).prefetch_related(
            'tags',
            'ingredients',
            'foreign_recipes',
            'shopping_cart',
            'favorite_recipe',
        )
