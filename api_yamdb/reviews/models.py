from django.db import models


class Titles (models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField('Год')
    rating = models.FloatField('Рейтинг')
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category (models.Model):
    name = models.CharField('Категория', max_length=200)
    slug = models.SlugField('Идентификатор', max_length=200)
    title = models.ForeignKey(Titles, related_name='category')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre (models.Model):
    name = models.CharField('Жанр', max_length=200)
    slug = models.SlugField('Идентификатор', max_length=200)
    title = models.ManyToManyField(Titles, related_name='genre')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name
