from django.urls import path, include
from .import views

urlpatterns = [

    # view 관련 내용과 api 관련 내용을
    # config.urls.views , config.urls.apis 모듈에 각각 분리 후
    # confing.urls.__init__에서 적절히 include처리

    # view
    path('', include('config.urls.views')),
    # api
    path('api/', include('config.urls.apis')),
]

