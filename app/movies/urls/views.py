
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from movies.views.pages import main_page
from movies.views.pages import main_genre_page


urlpatterns = [
    path('main_page_by_date',main_page, name='main_page_by_date'),
    path('main_page_by_genre',main_genre_page, name='main_page_by_genre'),
]+ static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

