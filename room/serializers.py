from rest_framework import serializers
from .models import Wing, Room


class WingSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = obj.image.url
            if request:
                return request.build_absolute_uri(image_url)
            return image_url
        return None

    class Meta:
        model = Wing
        fields = ('id', 'name', 'description', 'image')


class RoomSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = obj.image.url
            if request:
                return request.build_absolute_uri(image_url)
            return image_url
        return None

    class Meta:
        model = Room
        fields = (
            'id', 'title', 'description', 'price_per_night',
            'wing', 'category', 'image', 'beds', 'bedrooms',
            'bathrooms', 'guests', 'created_at'
        )
