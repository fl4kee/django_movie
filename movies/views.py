import math

from django.db.models import Q, Avg
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView

from movies.models import Movie, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm


class GenreYear():
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MovieView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'
    paginate_by = 3


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    template_name='movies/moviesingle.html'
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating = Rating.objects.filter(movie=self.object).aggregate(Avg('star'))

        context['star_form'] = RatingForm()
        print(rating)
        context['rating'] = str(math.floor(rating['star__avg'])) if rating['star__avg'] else '-1'
        context['form'] = ReviewForm()
        return context


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()

        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    template_name = 'movies/movies.html'
    paginate_by = 2
    def get_queryset(self):
        years = self.request.GET.getlist("year")
        genres = self.request.GET.getlist("genre")
        if years and genres:
            queryset = Movie.objects.filter(year__in=years, genres__in=genres)
        else:
            queryset = Movie.objects.filter(
                Q(year__in=years) |
                Q(genres__in=genres)
            ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist('genre')])
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        years = self.request.GET.getlist("year")
        genres = self.request.GET.getlist("genre")
        if years and genres:
            queryset = Movie.objects.filter(
                year__in=years,
                genres__in=genres
            ).distinct().values('title', 'tagline', 'url', 'poster')
        else:
            queryset = Movie.objects.filter(
                Q(year__in=years) |
                Q(genres__in=genres)
            ).distinct().values('title', 'tagline', 'url', 'poster')
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)

class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            print('HERE')
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)

        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 3
    template_name = 'movies/movies.html'

    def get_queryset(self):
        return Movie.objects.filter(title__contains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context