from rest_framework import serializers
from .models import Wing, Room
import os


class WingSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Wing
        fields = ('id', 'name', 'description', 'image_url')


class RoomSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Room
        fields = ('id', 'title', 'description', 'price_per_night',
                  'wing', 'category', 'image_url', 'beds', 'bedrooms', 'bathrooms', 'guests', 'created_at')
