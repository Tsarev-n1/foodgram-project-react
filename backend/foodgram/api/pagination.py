from rest_framework.pagination import PageNumberPagination


class CustomPaginatoion(PageNumberPagination):
    page_size = 6

    def get_page_size(self, request):
        limit = request.query_params.get('limit')
        if limit:
            return limit
        return super().get_page_size(request)
