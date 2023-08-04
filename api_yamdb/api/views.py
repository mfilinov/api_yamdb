from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.permissions import SAFE_METHODS

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer, TitleGetSerializer,
)
from reviews.models import Title, Category, Genre, Review
from users.permissions import (IsAdminUser, IsModeratorUser, IsOwnerOrReadOnly,
                               IsAdminUserOrReadOnly)
from .paginatiors import ResponsePaginator


class TitleViewSet(viewsets.ModelViewSet):
    # Запрещен method PUT
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options',
                         'trace']
    # Order необходим чтобы не было UnorderedObjectListWarning
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    pagination_class = ResponsePaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleGetSerializer
        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = ResponsePaginator
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminUserOrReadOnly]


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
