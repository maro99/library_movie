from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieMainSerializer, MovieMainGenreSerializer, MovieMainDistamceSerializer


class MovieListByDate(APIView):

    def get(self, request, format=None):
        movies = Movie.objects.order_by('when')

        # 날짜 지난 친구들은 안보여주겠다면 주석 풀어라
        # movies_filtered = list()
        # now = timezone.now()
        # for movie in movies:
        #     if movie.when >= now:
        #         movies_filtered.append(movie)

        serializer = MovieMainSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieListByGenre(APIView):

    def get(self, request, format=None):
        movies = Movie.objects.order_by('genre','when')

        # 날짜 지난 친구들은 안보여주겠다면 주석 풀어라
        # movies_filtered = list()
        # now = timezone.now()
        # for movie in movies:
        #     if movie.when >= now:
        #         movies_filtered.append(movie)

        serializer = MovieMainGenreSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieListByRating(APIView):

    def get(self, request, format=None):
        movies = Movie.objects.order_by('-rating')

        # 날짜 지난 친구들은 안보여주겠다면 주석 풀어라
        # movies_filtered = list()
        # now = timezone.now()
        # for movie in movies:
        #     if movie.when >= now:
        #         movies_filtered.append(movie)

        serializer = MovieMainGenreSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieListByDistance(APIView):

    def get(self, request, format=None):
        movies = Movie.objects.order_by('when')

        serializer = MovieMainDistamceSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
