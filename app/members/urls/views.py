from django.urls import path, include
from ..import views

app_name = 'members'

urlpatterns = [

    path('login_page/', views.login_page, name='login_page'),
    path('normal_login/', views.normal_login, name='normal_login'),
    path('logout_view/',views.logout_view, name='logout_view'),
    path('signup_page/', views.signup,name='signup_page'),
    path('activate/<str:uidb64>/<str:token>', views.user_activate, name='activate'),

    path('facebook_login/', views.facebook_login, name='facebook_login'),
    path('kakaotalk_login/', views.kakaotalk_login, name='kakaotalk_login'),
    path('naver_login/', views.naver_login, name='naver_login'),
    path('google_login/', views.google_login, name='google_login'),

    path('user_detail_page/', views.user_detail_page, name='user_detail_page'),
    path('user_info_change/', views.user_info_change_page, name='user_info_change_page'),
    path('user_password_change_page/', views.user_password_change_page, name='user_password_change_page'),
    path('user_password_change/<str:uidb64>/<str:token>/<str:password>', views.user_password_change, name='user_password_change'),
    path('user_email_change_page/', views.user_email_change_page, name='user_email_change_page'),
    path('user_email_change/<str:uidb64>/<str:token>/<str:email>', views.user_email_change,name='user_email_change'),
    path('user_phone_number_change_page/', views.user_phone_number_change_page, name='user_phone_number_change_page'),
    path('user_phone_number_change/<str:uidb64>/<str:token>/<str:phone_number>', views.user_phone_number_change, name='user_phone_number_change'),


]