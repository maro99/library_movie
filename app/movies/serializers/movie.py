from rest_framework import serializers

from movies.models import Movie
from .locations import LibrarySerializer


class MovieBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'pk',
            'title',
            'thumbnail_url',
            'when',
        )


class MovieMainSerializer(MovieBaseSerializer):
    pass


class MovieMainGenreSerializer(MovieBaseSerializer):

    class Meta(MovieBaseSerializer.Meta):
        fields = MovieBaseSerializer.Meta.fields + (
            'genre',
        )


class MovieDetailSerializer(MovieBaseSerializer):
    library = LibrarySerializer(read_only=True)

    class Meta(MovieBaseSerializer.Meta):
        fields = MovieBaseSerializer.Meta.fields + (
            'place',
            'runtime',
            'director',
            'age',
            'rating',
            'genre',
            'created_at',

            'library',

            'story',

        )



