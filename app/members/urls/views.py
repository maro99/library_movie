from django.urls import path
from ..import views

app_name = 'members'

urlpatterns = [

    path('login_page/', views.login_page, name='login_page'),
    path('normal_login/', views.normal_login, name='normal_login'),
    path('facebook_login/', views.facebook_login, name='facebook_login'),
    path('kakaotalk_login/', views.kakaotalk_login, name='kakaotalk_login'),
    path('naver_login/', views.naver_login, name='naver_login'),
    path('google_login/', views.google_login, name='google_login')
]