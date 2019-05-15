from django.urls import path

from movies import apis
from movies.apis import MovieListByDate, MovieDetail, MovieListByGenre, MovieListByRating, MovieListByDistance

app_name = 'movies-api'

urlpatterns = [
    path('main_page_by_date', MovieListByDate.as_view(), name='MovieListByDate'),
    path('main_page_by_genre', MovieListByGenre.as_view(), name='MovieListByGenre'),
    path('main_page_by_rating', MovieListByRating.as_view(), name='MovieListByRating'),
    path('main_page_by_distance', MovieListByDistance.as_view(), name='MovieListByDistance'),
    path('<int:pk>',MovieDetail.as_view(), name='MovieDetail'),

]