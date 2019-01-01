
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .. import views

app_name = 'movies'

urlpatterns = [
    path('main_page_by_date',views.main_page, name='main_page_by_date'),
    path('main_page_by_rating', views.main_rating_page, name='main_page_by_rating'),
    path('main_page_by_genre',views.main_genre_page, name='main_page_by_genre'),
    path('<int:pk>',views.movie_detail,name='movie_detail')
]+ static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

