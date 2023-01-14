from django.db.models import F
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.serializers import UserSerializer

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = UserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('__all__')

    def ingredient_amount_create(self, recipe, ingredients):
        for ingredient in ingredients:
            ingredient_obj = get_object_or_404(
                Ingredient,
                pk=ingredient['id']
            )
            count = ingredient['amount']
            RecipeIngredient.objects.get_or_create(
                ingredient=ingredient_obj,
                amount=count,
                recipe=recipe
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.ingredient_amount_create(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.ingredient_amount_create(instance, ingredients)
        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags'))
        return super().update(
            instance, validated_data)

    def validate_ingredients(self, value):
        if not value:
            return ValidationError({
                'Должен быть минимум 1 ингредиент!'
            })
        ingredient_list = []
        for item in value:
            ingredient = get_object_or_404(Ingredient, id=item['id'])
            if ingredient in ingredient_list:
                raise ValidationError({
                    'ingredients': 'Ингредиенты не должны повторяться!'
                })
            if int(item['amount']) <= 0:
                raise ValidationError({
                    'amount': 'Количество должно быть больше 0!'
                })
            ingredient_list.append(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError({
                'tags': 'Нужно выбрать тег!'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError({
                    'tags': 'Тег должен быть уникальным!'
                })
            tags_list.append(tag)
        return value


class IngredientViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        recipe = obj
        return recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredient__amount')
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()
