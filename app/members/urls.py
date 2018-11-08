from django.urls import path
from .views import *


urlpatterns = [

    path('login_page/', login_page, name='login_page'),
    path('login/', normal_login, name='login'),
    path('facebook_login/', facebook_login, name='facebook_login')
]