from rest_framework.pagination import PageNumberPagination


class UsersPaginator(PageNumberPagination):
    page_size = 10
