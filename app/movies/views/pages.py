from django.shortcuts import render

from movies.models import Movie
import datetime
from django.utils import timezone


def main_page(request):

    movies = Movie.objects.order_by("when")


    movies_filtered = movies

    # 날짜 지난 친구들은 안보여주겠다면 주석 풀어라
    # movies_filtered = list()
    # now = timezone.now()
    # for movie in movies:
    #     if movie.when >= now:
    #         movies_filtered.append(movie)


    context = {
        "movies":movies_filtered,

    }

    return render(request, 'movie/main.html',context=context)


def main_rating_page(request):

    movies = Movie.objects.order_by("-rating")

    movies_filtered = movies

    # 날짜 지난 친구들은 안보여주겠다면 주석 풀어라
    # movies_filtered = list()
    # now = timezone.now()
    # for movie in movies:
    #     if movie.when >= now:
    #         movies_filtered.append(movie)


    context = {
        "movies":movies_filtered,

    }

    return render(request, 'movie/main.html',context=context)


def main_genre_page(request):

    movies = Movie.objects.order_by("when")
    movies_filtered = movies

    # 날짜 지난 친구들은 안보여주겠다면 주석 풀어라
    # movies_filtered = list()
    # now = timezone.now()
    # for movie in movies:
    #     if movie.when >= now:
    #         movies_filtered.append(movie)


    # 장르 뽑아서 전달 해 주겠다.
    genre_list = []
    for movie in movies:
        if movie.genre not in genre_list:
            genre_list.append(movie.genre)


    print(genre_list)

    context = {
        "movies":movies_filtered,
        "genre_list":genre_list,
    }

    return render(request, 'movie/main_genre.html',context=context)


def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie':movie,
    }
    return render(request, 'movie/movie_detail.html', context)
