from django.db import models


class Movie (models.Model):
    title = models.CharField(max_length=200)
    when = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True)
    place = models.CharField(max_length=200,blank=True)

    # 이하는 네이버 영화 검색으로 넣을것.
    director = models.CharField(max_length=200)
    thumbnail_url = models.CharField(max_length=200)
    story = models.TextField(blank=True)
    age = models.CharField(max_length=200, blank=True)
    rating = models.FloatField(default=0, blank=True)