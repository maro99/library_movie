from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager as DjangoManager


class UserManager(DjangoManager): # 이렇게 오버라이드 해주면 UserManager동작을 우리가 언제든지 바꿀 수 있다.
    pass


class User(AbstractUser):
    img_profile = models.ImageField(upload_to="user", blank=True)
    password2 = models.CharField(max_length=255,blank=True)
    objects = UserManager()