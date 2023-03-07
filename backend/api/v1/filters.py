import django_filters as filters
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipe
from users.models import User


class IngredientsFilter(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(),
        label='В корзине.'
    )
    is_favorited = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(),
        label='В избранных.'
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='Ссылка'
    )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']
