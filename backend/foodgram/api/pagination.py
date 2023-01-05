from rest_framework.pagination import PageNumberPagination


class CustomPaginatoion(PageNumberPagination):
    page_size = 6
