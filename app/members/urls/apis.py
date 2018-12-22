from django.urls import path

from members import apis
from members.apis import UserList

app_name = 'members-api'

urlpatterns = [
    path('', UserList.as_view()),
    path('auth-token', apis.AuthToken.as_view()),
    path('auth-test', apis.AuthenticationTest.as_view()),
    path('signup', apis.Signup.as_view()),
    path('activate/<str:uidb64>/<str:token>', apis.UserActivate.as_view(), name='activate'),

    path('user-info-change-page', apis.UserInfoChangePageView.as_view(), name='user-info-change-page'),
    path('user-info-change-page/password-change', apis.UserChangePasswordView.as_view(), name='user-password-change'),
    path('user-info-change-page/email-change', apis.UserChangeEmailView.as_view(), name='user-email-change'),

]