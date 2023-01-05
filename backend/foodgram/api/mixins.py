from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin


class ViewOnlyMixin(GenericViewSet, ListModelMixin):
    pass
