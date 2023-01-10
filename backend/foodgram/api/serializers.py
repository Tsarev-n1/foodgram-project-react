from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField

from django.shortcuts import get_object_or_404
from django.db.models import F

from .models import Recipe, Tag, RecipeIngridient, Ingridient
from users.serializers import UserSerializer


class RecipeIngridientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngridient
        fields = ['id', 'amount']


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingridients = RecipeIngridientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = UserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('__all__')

    def ingridient_amount_create(self, recipe, ingridients):
        for ingridient in ingridients:
            ingridient_obj = get_object_or_404(
                Ingridient,
                pk=ingridient['id']
            )
            count = ingridient['amount']
            RecipeIngridient.objects.get_or_create(
                ingridient=ingridient_obj,
                amount=count,
                recipe=recipe
            )

    def create(self, validated_data):
        ingridients = validated_data.pop('ingridients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.ingridient_amount_create(recipe, ingridients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        if 'ingridients' in validated_data:
            ingridients = validated_data.pop('ingridients')
            instance.ingridients.clear()
            self.ingridient_amount_create(instance, ingridients)
        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags'))
        return super().update(
            instance, validated_data)

    def validate_ingridients(self, value):
        if not value:
            return ValidationError({
                'Должен быть минимум 1 ингридиент!'
            })
        list = []
        for item in value:
            ingredient = get_object_or_404(Ingridient, id=item['id'])
            if ingredient in list:
                raise ValidationError({
                    'ingredients': 'Ингридиенты не должны повторяться!'
                })
            if int(item['amount']) <= 0:
                raise ValidationError({
                    'amount': 'Количество должно быть больше 0!'
                })
            list.append(ingredient)
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


class IngridientViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
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
    ingridients = serializers.SerializerMethodField()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingridients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingridients(self, obj):
        recipe = obj
        ingridients = recipe.ingridients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingridient__amount')
        )
        return ingridients

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
