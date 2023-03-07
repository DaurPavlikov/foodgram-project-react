from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from recipes.models import Recipe
from .serializers import SubscribeRecipeSerializer


class GetObjectMixin:
    """Миксина для добавления и удаления понравившихся рецептов в корзине."""

    serializer_class = SubscribeRecipeSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.check_object_permissions(self.request, recipe)
        return recipe


class GetIsSubscribedMixin:
    """Миксина для проверки подписки пользователя."""

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.follower.filter(author=obj).exists()
