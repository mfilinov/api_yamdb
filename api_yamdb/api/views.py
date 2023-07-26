from rest_framework import viewsets

from .mixins import CreateListViewSet
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from reviews.models import Title, Category, Genre


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    ...


class ReviewViewSet(viewsets.ModelViewSet):
    ...
