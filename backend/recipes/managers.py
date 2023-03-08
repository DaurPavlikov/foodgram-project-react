from django.db.models import Manager


class RecipesRelationManager(Manager):
    def get_relations(self):
        return super().select_related(
            'author'
        ).prefetch_related(
            'tags',
            'foreign_ingredients',
            'foreign_recipes',
            'shopping_cart',
            'favorite_recipes',
        )
