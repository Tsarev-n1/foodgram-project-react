from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS
)
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .permissions import IsAuthorOrReadOnly
from .pagination import CustomPaginatoion
from .models import (
    Recipe,
    Ingridient, Tag,
    Favourite, ShoppingCart,
    RecipeIngridient
)
from .serializers import (
    RecipeWriteSerializer,
    IngridientViewSerializer,
    TagSerializer, RecipeShortSerializer,
    RecipeReadSerializer
)
from .filters import IngredientFilter, RecipeFilter
from .mixins import ViewOnlyMixin


class RecipeViewCreate(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly | IsAdminUser]
    pagination_class = CustomPaginatoion
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Favourite, request.user, pk)
        else:
            return self.delete_from(Favourite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        else:
            return self.delete_from(ShoppingCart, request.user, pk)

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingridients = RecipeIngridient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingridient__name',
            'ingridient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        today = datetime.today()
        shopping_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingridient["ingridient__name"]} '
            f'({ingridient["ingridient__measurement_unit"]})'
            f' - {ingridient["amount"]}'
            for ingridient in ingridients
        ])
        shopping_list += f'\n\nFoodgram ({today:%Y})'

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class IngridientView(ViewOnlyMixin):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientViewSerializer
    pagination_class = CustomPaginatoion
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagView(ViewOnlyMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
