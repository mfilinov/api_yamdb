from django.db import models


class Title (models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год')
    rating = models.FloatField('Рейтинг')
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category (models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Идентификатор', unique=True, max_length=50)
    title = models.ForeignKey(Title, related_name='category')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre (models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField('Идентификатор', unique=True, max_length=50)
    title = models.ManyToManyField(Title, related_name='genre')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name
