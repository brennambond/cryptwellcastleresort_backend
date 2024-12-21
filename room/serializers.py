from rest_framework import serializers
from .models import Wing, Room


class WingSerializer(serializers.ModelSerializer):
    image_url_full = serializers.ReadOnlyField()

    class Meta:
        model = Wing
        fields = ('id', 'name', 'description', 'image_url', 'image_url_full')


class RoomSerializer(serializers.ModelSerializer):
    image_url_full = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = ('id', 'title', 'description', 'price_per_night',
                  'wing', 'category', 'image_url', 'image_url_full', 'beds', 'bedrooms', 'bathrooms', 'guests', 'created_at')
