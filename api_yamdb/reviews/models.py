from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api_yamdb.settings import TEXT_MAX_LENGTH

User = get_user_model()


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveIntegerField('Год')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField('Genre', blank=True, related_name='title')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Идентификатор', unique=True, max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField('Идентификатор', unique=True, max_length=50)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва на произведение."""
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.PositiveIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, message='Ваша оценка ниже допустимой'),
            MaxValueValidator(10, message='Ваша оценка выше допустимой')
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:TEXT_MAX_LENGTH]


class Comment(models.Model):
    """Модель комментария к отзыву."""
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_MAX_LENGTH]
