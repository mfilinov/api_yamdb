from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Category, Genre, Comment, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug')
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        serializer = TitleGetSerializer(instance)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Запрещает дублирование отзыва."""
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(
                    author=self.context.get('request').user,
                    title=self.context.get('view').kwargs.get('title_id')
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
