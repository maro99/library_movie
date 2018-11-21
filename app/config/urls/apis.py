from django.urls import path, include

urlpatterns = [
    # apii
    # path('posts/', incldue('posts.urls.apis')),
    path('users/',include('members.urls.apis')),
]