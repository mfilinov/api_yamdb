from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitlePostSerializer
)
from reviews.models import Title, Category, Genre, Review
from users.permissions import (IsAdminUser, IsModeratorUser, IsOwnerOrReadOnly,
                               IsAdminUserOrReadOnly)
from .paginatiors import ResponsePaginator


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = ResponsePaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitlePostSerializer
        return TitleSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@action(methods=['get', 'post', 'delete'], detail=False)
class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = ResponsePaginator
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminUserOrReadOnly]


@action(methods=['get', 'post', 'delete'], detail=False)
class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = ResponsePaginator
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminUserOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзывов Review."""

    serializer_class = ReviewSerializer
    pagination_class = ResponsePaginator
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser | IsModeratorUser]

    def get_title(self):
        """Возвращает объект текущего произведения."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""
        return self.get_title().reviews.select_related('author')

    def perform_create(self, serializer):
        """Создает отзыв для текущего произведения."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели комментариев Comment."""

    serializer_class = CommentSerializer
    pagination_class = ResponsePaginator
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser | IsModeratorUser]

    def get_review(self):
        """Возвращает объект текущего отзыва."""
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        """Создает комментарий для текущего отзыва"""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
