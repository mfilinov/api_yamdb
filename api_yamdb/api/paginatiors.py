from rest_framework.pagination import PageNumberPagination


class ResponsePaginator(PageNumberPagination):
    page_size = 10
