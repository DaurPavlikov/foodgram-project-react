from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import mark_safe

from .managers import RecipesRelatedManager

MIN_COOKING_TIME = 1
MIN_INGREDIENT_AMT = 1

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингридиента, для описания названия и его единицы измерения."""

    name = models.CharField('Название ингредиента', max_length=255)
    measurement_unit = models.CharField('Единица измерения', max_length=64)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Tag(models.Model):
    """Модель тэга, для сортировки рецептов."""

    name = models.CharField('Название', max_length=64, unique=True)
    color = models.CharField('Цвет в HEX', max_length=7, unique=True)
    slug = models.SlugField('Ссылка', max_length=127, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', args=[self.slug])


class Recipe(models.Model):
    """Модель рецепта. Содержит ссылки на все основные модели проекта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='foreign_recipes',
        verbose_name='Автор'
    )
    name = models.CharField('Название рецепта', max_length=255)
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipes/',
        blank=True,
        null=True
    )
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='many_ingredients'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[validators.MinValueValidator(
            MIN_COOKING_TIME,
            message=f'Мин. время приготовления {MIN_COOKING_TIME} минута',
        ), ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    objects = models.Manager()
    recipes_related = RecipesRelatedManager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def image_tag(self):
        return mark_safe(
            '<img src="/directory/%s" width="150" height="150" />'
            % (self.image)
        )
    image_tag.short_description = 'Image'

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class RecipeIngredient(models.Model):
    """Модель связи рецепта и используемого в нём ингридиента."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='foreign_recipes'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='foreign_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        default=MIN_INGREDIENT_AMT,
        validators=(
            validators.MinValueValidator(
                MIN_INGREDIENT_AMT,
                message=f'Мин. количество ингридиентов {MIN_INGREDIENT_AMT}',
            ),
        ),
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient',
            )
        ]


class Subscribe(models.Model):
    """Модель подписки пользователя на автора рецепта."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    created = models.DateTimeField('Дата подписки', auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class FavoriteRecipe(models.Model):
    """Модель для добавления рецептов в раздел избранного."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite_recipe',
        verbose_name='Пользователь',
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в избранное.'

    @receiver(post_save, sender=User)
    def create_favorite_recipe(sender, instance, created, **kwargs):
        if created:
            return FavoriteRecipe.objects.create(user=instance)


class ShoppingCart(models.Model):
    """Модель для добавления рецептов в список покупок."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
        verbose_name='Пользователь'
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Покупка'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-id']

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в список покупок.'

    @receiver(post_save, sender=User)
    def create_shopping_cart(sender, instance, created, **kwargs):
        if created:
            return ShoppingCart.objects.create(user=instance)
