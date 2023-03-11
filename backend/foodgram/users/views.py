from api.pagination import CustomPaginatoion
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .mixins import UserMixin
from .models import Follow
from .serializers import FollowSerializer, UserSerializer

User = get_user_model()


class UserViewSet(UserMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPaginatoion

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = Follow.objects.filter(user=user)
        return FollowSerializer(subscriptions, many=True).data

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('pk')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = FollowSerializer(author,
                                          data=request.data,
                                          context={"request": request})
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        subscription = get_object_or_404(Follow,
                                         user=user,
                                         author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
