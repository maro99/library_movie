from django.contrib import admin

# Register your models here.
from movies.models import Movie, Library, District

admin.site.register(Movie)
admin.site.register(Library)
admin.site.register(District)