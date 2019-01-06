from django.urls import path

from movies import apis
from movies.apis import MovieListByDate, MovieDetail, MovieListByGenre, MovieListByRating

app_name = 'movies-api'

urlpatterns = [
    path('main_page_by_date', MovieListByDate.as_view(), name='MovieListByDate'),
    path('main_page_by_genre', MovieListByGenre.as_view(), name='MovieListByGenre'),
    path('main_page_by_rating', MovieListByRating.as_view(), name='MovieListByRating'),
    path('<int:pk>',MovieDetail.as_view(), name='MovieDetail'),

    # path('auth-token', apis.AuthToken.as_view()),
    # path('auth-test', apis.AuthenticationTest.as_view()),
    # path('signup', apis.Signup.as_view()),
    # path('activate/<str:uidb64>/<str:token>', apis.UserActivate.as_view(), name='activate'),
    #
    # path('user-info-change-page', apis.UserInfoChangePageView.as_view(), name='user-info-change-page'),
    # path('user-info-change-page/password-change', apis.UserChangePasswordView.as_view(), name='user-password-change'),
    # path('user-info-change-page/email-change', apis.UserChangeEmailView.as_view(), name='user-email-change'),
    # path('user-info-change-page/phone-number-change',
    #      apis.UserChangePhoneNumberView.as_view(), name='user-phone-number--change'),

]