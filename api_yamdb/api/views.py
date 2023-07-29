from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import filters, viewsets, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .mixins import CreateListViewSet

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitlePostSerializer
)
from reviews.models import Title, Category, Genre, Review


class TitleFilter(rest_framework.FilterSet):
    genre = rest_framework.CharFilter(field_name='genre__slug',
                                      lookup_expr='iexact')
    category = rest_framework.CharFilter(field_name='category__slug',
                                         lookup_expr='iexact')
    year = rest_framework.NumberFilter(field_name='year', lookup_expr='iexact')
    name = rest_framework.CharFilter(field_name='name', lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitlePostSerializer
        return TitleSerializer

    def partial_update(self, request, *args, **kwargs):
        title = self.get_object()
        serializer = self.get_serializer(title, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        title = self.get_object()
        average_score = title.reviews.aggregate(Avg('score'))['score__avg']
        title.rating = average_score
        serializer = self.get_serializer(title)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            queryset = queryset.annotate(
                aggregate_rating=Avg('reviews__score')
            )
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    '''@permission_classes([IsAdminUser])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @permission_classes([IsAdminUser])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)'''

    def get_permissions(self):
        if self.action == 'create' or self.action == 'delete':
            return (permissions.IsAdminUser,)
        return super().get_permissions()


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


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
