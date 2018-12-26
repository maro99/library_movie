from django.shortcuts import render

from movies.models import Movie


def main_page(request):

    movies=Movie.objects.all()

    context = {
        "movies":movies
    }
    return render(request, 'movie/main.html',context=context)

