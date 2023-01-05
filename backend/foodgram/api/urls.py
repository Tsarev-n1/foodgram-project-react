from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewCreate, IngridientView, TagView

app_name = 'api'

router = DefaultRouter()

router.register(r'recipes', RecipeViewCreate, basename='recipes')
router.register(r'ingridients', IngridientView, basename='ingridients')
router.register(r'tags', TagView, basename='tags')


urlpatterns = [
    path('', include(router.urls))
]
