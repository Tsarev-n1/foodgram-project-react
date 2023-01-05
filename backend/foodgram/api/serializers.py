from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from django.shortcuts import get_object_or_404
from django.db.models import F

from .models import Recipe, Tag, RecipeIngridient, RecipeTag, Ingridient

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

    def create(self, validated_data):
        ingridients = validated_data.pop('ingridients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingridient in ingridients:
            ingridient_obj = get_object_or_404(
                Ingridient,
                pk=ingridient.get('id')
            )
            count = ingridient.get('amount')
            RecipeIngridient.objects.get_or_create(
                ingridient=ingridient_obj,
                amount=count,
                recipe=recipe
            )
        for tag in tags:
            tag_obj = get_object_or_404(Tag, pk=tag)
            RecipeTag.objects.get_or_create(tag=tag_obj, recipe=recipe)
        return recipe


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
            amount=F('recipeingridient__amount')
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
