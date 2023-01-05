from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.db.models import UniqueConstraint


def get_user_media_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.author.id, instance.id)


class Recipe(models.Model):

    name = models.CharField('Название рецепта', max_length=50)
    image = models.ImageField(
        'Изображение',
        upload_to=get_user_media_path
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    text = models.TextField('Описание', max_length=200)
    ingridients = models.ManyToManyField(
        'Ingridient',
        through='RecipeIngridient'
    )
    tags = models.ManyToManyField('Tag', through='RecipeTag')
    cooking_time = models.FloatField(
        'Время приготовления',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Tag(models.Model):

    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(
        unique=True,
        max_length=50,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не является цветом в формате HEX!'
            )]
    )
    slug = models.SlugField(unique=True)


class Ingridient(models.Model):

    name = models.CharField(
        'Название ингридиента',
        unique=True,
        max_length=50
    )

    measurement_unit = models.CharField('Единица измерения', max_length=20)


class RecipeTag(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class RecipeIngridient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingridient_list',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(1, message='Минимальное количество 1!')],
    )
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецептах'

    def __str__(self):
        return (
            f'{self.ingridient.name} ({self.ingridient.measurement_unit})'
            f' - {self.amount} '
        )


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favourite')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
