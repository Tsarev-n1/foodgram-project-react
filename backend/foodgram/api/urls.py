from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientView, RecipeViewCreate, TagView

app_name = 'api'

router = DefaultRouter()

router.register(r'recipes', RecipeViewCreate, basename='recipes')
router.register(r'ingredients', IngredientView, basename='ingredients')
router.register(r'tags', TagView, basename='tags')


urlpatterns = [
    path('', include(router.urls))
]
