from django.db import models


class District(models.Model):
    district_name = models.CharField(max_length=100)


class Library(models.Model):
    library_name = models.CharField(max_length=100)
    library_code = models.CharField(max_length=100)
    library_district = models.ForeignKey(District,related_name='library', on_delete=models.CASCADE)

    library_address = models.CharField(max_length=1000, blank = True)
    lat = models. FloatField(default=0, blank=True)
    lng = models.FloatField(default=0, blank=True)