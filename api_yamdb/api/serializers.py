from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Title, Category, Genre, Comment, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug')
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    rating = serializers.FloatField(required=False, default=None)
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        if Genre.objects.filter(slug__in=genres).exists():
            title.genre.set(Genre.objects.filter(slug__in=genres))
            return title
        return title


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    rating = serializers.FloatField(required=False, default=None)
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')

    def get_genre(self, obj):
        genres = obj.genre.all()
        return [{'name': genre.name, 'slug': genre.slug} for genre in genres]

    def get_category(self, obj):
        category = obj.category
        if category is not None:
            return {'name': category.name, 'slug': category.slug}
        return None

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        if Genre.objects.filter(slug__in=genres).exists():
            title.genre.set(Genre.objects.filter(slug__in=genres))
            return title
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для модели Review."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        queryset=Title.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['title']
        #  Каждый пользователь может оставить только один отзыв на произведение
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer для модели Comment."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['review']
