from django.urls import path
from .views import *


urlpatterns = [

    path('login_page/', login_page, name='login_page'),
    path('normal_login/', normal_login, name='normal_login'),
    path('facebook_login/', facebook_login, name='facebook_login'),
    path('kakaotalk_login/', kakaotalk_login, name='kakaotalk_login')
]