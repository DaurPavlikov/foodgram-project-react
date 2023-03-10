from rest_framework.pagination import PageNumberPagination


class LimitPagination(PageNumberPagination):
    """Основной пагинатор для проекта."""

    page_size = 6
    page_size_query_param = 'limit'
