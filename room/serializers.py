from rest_framework import serializers
from .models import Wing, Room
import os


class WingSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        bucket_domain = os.getenv(
            "AWS_S3_CUSTOM_DOMAIN", "hauntedhotel-backend-bucket.s3.amazonaws.com"
        )
        return f"https://{bucket_domain}/{obj.image_url.name}" if obj.image_url else None

    class Meta:
        model = Wing
        fields = ('id', 'name', 'description', 'image_url')


class RoomSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        bucket_domain = os.getenv(
            "AWS_S3_CUSTOM_DOMAIN", "hauntedhotel-backend-bucket.s3.amazonaws.com"
        )
        if obj.image and obj.image.name != "uploads/default-room.png":
            return f"https://{bucket_domain}/{obj.image.name}"
        return None  # Return None if the default image is used

    class Meta:
        model = Room
        fields = ('id', 'title', 'description', 'price_per_night',
                  'wing', 'category', 'image_url', 'beds', 'bedrooms', 'bathrooms', 'guests', 'created_at')
