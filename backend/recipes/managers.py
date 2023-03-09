from django.db import models
from rest_framework import status
from rest_framework.response import Response


class RecipesRelatedManager(models.Manager):
    """Менеджер для получения списка рецептов со всеми связанными моделями."""

    def get_queryset(self):
        tags = self.request.query_params.getlist('tags')
        if tags:
            return super().get_queryset().filter(
                tags__slug__in=tags
            ).distinct().select_related(
                'author'
            ).prefetch_related(
                'tags',
                'ingredients',
                'foreign_recipes',
                'shopping_cart',
                'favorite_recipe',
            )
        return Response('Теги не выбраны.', status=status.HTTP_204_NO_CONTENT)
