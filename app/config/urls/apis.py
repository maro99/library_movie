from django.urls import path, include

urlpatterns = [
    # apii
    # path('posts/', incldue('posts.urls.apis')),
    path('members/',include('members.urls.apis')),
]