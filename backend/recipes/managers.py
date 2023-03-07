from django.db.models import Manager


class RecipesRelationManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'author'
        ).prefetch_related(
            'tags',
            'ingredients',
            'recipes',
            'shopping_cart',
            'favorite_recipes',
        )
