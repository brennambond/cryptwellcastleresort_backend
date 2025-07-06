from rest_framework import serializers
from .models import Wing, Room


class WingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wing
        fields = ('id', 'name', 'description', 'image_url')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id', 'title', 'description', 'price_per_night',
            'wing', 'category', 'image_url', 'beds', 'bedrooms',
            'bathrooms', 'guests', 'created_at'
        )
