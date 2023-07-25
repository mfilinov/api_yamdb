from .models import Title, Category, Genre
from django.views import generic


class TitleListView(generic.ListView):
    model = Title
    fields = '__all__'
    paginate_by = 10
    ordering = 'name'


class TitleDetailView(generic.DetailView):
    model = Title
    fields = '__all__'


class TitleCreateView(generic.CreateView):
    model = Title
    fields = '__all__'


class TitleUpdateView(generic.UpdateView):
    model = Title
    fields = '__all__'


class TitleDeleteView(generic.DeleteView):
    model = Title


class CategoryListView(generic.ListView):
    model = Category
    fields = '__all__'
    paginate_by = 10
    ordering = 'name'


class CategoryCreateView(generic.CreateView):
    model = Category
    fields = '__all__'


class CategoryDeleteView(generic.DeleteView):
    model = Category


class GenreListView(generic.ListView):
    model = Genre
    fields = '__all__'
    paginate_by = 10
    ordering = 'name'


class GenreCreateView(generic.CreateView):
    model = Genre
    fields = '__all__'


class GenreDeleteView(generic.DeleteView):
    model = Genre
