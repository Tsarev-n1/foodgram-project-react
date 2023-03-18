from rest_framework.pagination import PageNumberPagination


class CustomPaginatoion(PageNumberPagination):
    page_size = 6

    def get_page_size(self, request):
        if request.query_params.get('is_in_shopping_cart'):
            return None
        return super().get_page_size(request)