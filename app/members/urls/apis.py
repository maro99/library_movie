from django.urls import path

from members import apis

app_name = 'members-api'

urlpatterns = [
    path('auth-token/', apis.AuthToken.as_view()),
    # path('auth-test/'), apis.A
]