from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager as DjangoManager

from movies.models import Movie


class UserManager(DjangoManager): # 이렇게 오버라이드 해주면 UserManager동작을 우리가 언제든지 바꿀 수 있다.
    pass


class User(AbstractUser):
    img_profile = models.ImageField(upload_to="user", blank=True)
    password2 = models.CharField(max_length=255,blank=True)
    phone_number = models.CharField(max_length=255,blank=True)
    movie = models.ManyToManyField(Movie,through='MovieLike',blank=True)
    objects = UserManager()
    set_alarm_before_24h = models.BooleanField(default=False)
    set_alarm_before_3h = models.BooleanField(default=False)

    @property
    def like_movies(self):
        like_movie_list = list()

        for movielike in self.movielike_set.all():
            like_movie_list.append(movielike.movie)

        return like_movie_list


class MovieLike(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
   )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
