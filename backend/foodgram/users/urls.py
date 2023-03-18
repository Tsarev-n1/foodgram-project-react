from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'users'

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/',
        UserViewSet.as_view({'get': 'subscriptions'})
    ),
    path(
        'users/<pk>/subscribe/',
        UserViewSet.as_view({'post': 'subscribe'})
    ),
    path(
        'users/<pk>/subscribe/',
        UserViewSet.as_view({'delete': 'subscribe'})
    ),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
