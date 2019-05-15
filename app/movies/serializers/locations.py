from rest_framework import serializers

from ..models.locations import Library, District


class DistrictBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = (
            'district_name',
        )


class DistrictSerializer(DistrictBaseSerializer):
    pass


class LibraryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = (
            'pk',
            'library_name',
        )


class LibrarySerializer(LibraryBaseSerializer):
    pass


class LibraryExtraInfoSerializer(LibraryBaseSerializer):
    library_district = DistrictSerializer(read_only=True)

    class Meta(LibraryBaseSerializer.Meta):
        fields = LibraryBaseSerializer.Meta.fields + (
            'library_code',
            'library_district',
            'library_address',
            'lat',
            'lng',
        )


class LibraryDistanceSerializer(LibraryBaseSerializer):

    class Meta(LibraryBaseSerializer.Meta):
        fields = LibraryBaseSerializer.Meta.fields + (
            'lat',
            'lng',
        )



