from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Title, Category, Genre, Comment, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


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
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            if Genre.objects.filter(slug=genre.slug).exists():
                title.genre.add(genre)
        return title


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
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

    def get_rating(self, obj):
        average_score = obj.reviews.aggregate(Avg('score'))['score__avg']
        return average_score

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
