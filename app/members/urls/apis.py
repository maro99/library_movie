from django.urls import path

from members import apis
from members.apis import UserList

app_name = 'members-api'

urlpatterns = [
    path('', UserList.as_view()),
    path('auth-token/', apis.AuthToken.as_view()),
    # path('auth-test/'), apis.A
]