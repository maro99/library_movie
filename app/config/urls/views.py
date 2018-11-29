
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from members import views

urlpatterns = [
    path('',views.login_page, name='login_page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('members/',include('members.urls.views') ),
]+ static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
