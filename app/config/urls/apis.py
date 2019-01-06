from django.urls import path, include

urlpatterns = [
    # apii
    path('movies/', include('movies.urls.apis')),
    path('members/',include('members.urls.apis')),
]