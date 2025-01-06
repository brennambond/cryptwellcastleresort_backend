from rest_framework import serializers
from .models import Wing, Room
import os


class WingSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        bucket_domain = os.getenv(
            "AWS_S3_CUSTOM_DOMAIN", "hauntedhotel-backend-bucket.s3.us-east-1.amazonaws.com"
        )
        return f"https://{bucket_domain}/{obj.image_url.name}" if obj.image_url else None

    class Meta:
        model = Wing
        fields = ('id', 'name', 'description', 'image_url')


class RoomSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        bucket_domain = os.getenv(
            "AWS_S3_CUSTOM_DOMAIN", "hauntedhotel-backend-bucket.s3.us-east-1.amazonaws.com"
        )
        if obj.image and obj.image.name:
            image_url = f"https://{bucket_domain}/{obj.image.name}"
            # Debugging
            print(f"Serialized Image URL for {obj.title}: {image_url}")
            return image_url
        print(f"No image for {obj.title}, returning None")  # Debugging
        return None

    class Meta:
        model = Room
        fields = ('id', 'title', 'description', 'price_per_night',
                  'wing', 'category', 'image_url', 'beds', 'bedrooms', 'bathrooms', 'guests', 'created_at')
