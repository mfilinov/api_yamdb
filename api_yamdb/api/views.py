from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .mixins import CreateListViewSet

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from reviews.models import Title, Category, Genre, Review


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзывов Review."""

    serializer_class = ReviewSerializer

    def get_title(self):
        """Возвращает объект текущего произведения."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает отзыв для текущего произведения."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели комментариев Comment."""

    serializer_class = CommentSerializer

    def get_review(self):
        """Возвращает объект текущего отзыва."""
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает комментарий для текущего отзыва"""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
