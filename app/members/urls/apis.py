from django.urls import path

from members import apis
from members.apis import UserList

app_name = 'members-api'

urlpatterns = [
    path('', UserList.as_view()),
    path('login', apis.Login.as_view()),
    path('auth-test', apis.AuthenticationTest.as_view()),
    path('signup', apis.Signup.as_view()),
    path('signout', apis.SignoutView.as_view()),
    path('activate/<str:uidb64>/<str:token>', apis.UserActivate.as_view(), name='activate'),

    path('user-info-change-page', apis.UserInfoChangePageView.as_view(), name='user-info-change-page'),
    path('user-info-change-page/password-change', apis.UserChangePasswordView.as_view(), name='user-password-change'),
    path('user-info-change-page/email-change', apis.UserChangeEmailView.as_view(), name='user-email-change'),
    path('user-info-change-page/phone-number-change',
         apis.UserChangePhoneNumberView.as_view(), name='user-phone-number--change'),

    path('movie-like-page', apis.UserMovieLikeList.as_view(), name='movie-like-page'),
    path('movie-like/<int:pk>', apis.UserMovieLike.as_view(), name='movie-like'),

    path('logout', apis.LogoutView.as_view(), name='logout'),

    path('signup-server-test', apis.SignupServerTest.as_view()),

    path('google-auth-token', apis.GoogleAuthToken.as_view()),
]