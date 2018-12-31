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
        "movies":movies_filtered
    }
    return render(request, 'movie/main.html',context=context)

