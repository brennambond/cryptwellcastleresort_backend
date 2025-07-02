from rest_framework import serializers
from .models import Wing, Room


class WingSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Wing
        fields = ('id', 'name', 'description', 'image')


class RoomSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Room
        fields = (
            'id', 'title', 'description', 'price_per_night', 'wing', 'category',
            'image', 'beds', 'bedrooms', 'bathrooms', 'guests', 'created_at'
        )
