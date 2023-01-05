from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin


class UserMixin(GenericViewSet, ListModelMixin, CreateModelMixin):
    pass
