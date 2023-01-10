from django.contrib import admin

from .models import (
    Favourite, Ingridient,
    RecipeIngridient, Recipe,
    ShoppingCart
)


class RecipeIngridientInline(admin.TabularInline):
    model = Recipe.ingridients.through
    extra = 1


@admin.register(RecipeIngridient)
class RecipeIngridientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingridient',
        'recipe',
        'amount'
    )
    search_fields = ('recipe__name', 'ingridient__name')


@admin.register(Ingridient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = ('measurement_unit',)
    list_filter = ('measurement_unit',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngridientInline,)
    list_display = (
        'pk',
        'name',
        'author'
    )
    search_fields = (
        'name',
        'author__username',
        'author__email'
    )
    readonly_fields = ('is_favorited',)

    def is_favorited(self, instance):
        return instance.favorite_recipes.count()


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )
