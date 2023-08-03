from django.contrib import admin

from reviews.models import Title, Category, Genre, Review


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
        'get_genres'
    )
    list_editable = (
        'category',
    )
    search_fields = ('name',)

    def get_genres(self, obj):
        return '\n'.join([genre for genre in obj.genre.all()])

    get_genres.short_description = 'Жанры'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'score',
        'author',
        'title',
        'pub_date'
    )
    search_fields = ('name',)


admin.site.empty_value_display = 'Не задано'
