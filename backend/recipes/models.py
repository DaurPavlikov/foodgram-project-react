from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from .managers import RecipesRelationManager

MIN_COOKING_TIME = 1
MIN_INGREDIENT_AMT = 1

User = get_user_model()


class Ingredient(models.Model):
    """Модель Ингредиента. Содержит название и единицу измерения."""

    name = models.CharField('Название ингредиента', max_length=255)
    measurement_unit = models.CharField('Единица измерения', max_length=64)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Tag(models.Model):
    """Модель Тэга. Применяется для сортировки выдачи рецептов."""

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
    """Модель Рецепта. Комплексная модель включающая в себя все данные."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors_recipes',
        verbose_name='Автор'
    )
    name = models.CharField('Название рецепта', max_length=255)
    image = models.ImageField(
        'Фото рецепта',
        upload_to='media/recipes_images/',
        blank=True,
        null=True
    )
    text = models.TextField('Описание рецепта')
    cooking_time = models.BigIntegerField('Время приготовления рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='ingredients',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='tags'
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
    recipes_relation = RecipesRelationManager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class RecipeIngredient(models.Model):
    """Модель для связи модели Ингридиента с моделью Рецепта."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='ingredients'
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
    """Модель для связи подписчика с автором."""

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
    """Модель для связи модели Пользователя с его избранными рецептами."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite_recipes',
        verbose_name='Пользователь',
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='favorite_recipes',
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
    """Модель для связи модели Пользователя с его корзиной покупок."""

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
