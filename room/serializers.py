from rest_framework import serializers
from .models import Room, Wing, Category


class WingSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField(source='image_url')

    class Meta:
        model = Wing
        fields = ['id', 'name', 'description', 'image_url']


class WingsDetailSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()

    class Meta:
        model = Wing
        fields = ['id', 'name', 'description', 'image_url', 'rooms']

    def get_rooms(self, obj):
        from .serializers import RoomSerializer
        rooms = obj.room_set.all()
        return RoomSerializer(rooms, many=True, context=self.context).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class RoomSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField(source='image_url')
    availability_status = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = [
            'id', 'title', 'description', 'price_per_night', 'beds', 'bedrooms',
            'bathrooms', 'guests', 'category', 'wing', 'image_url', 'availability_status',
            'created_at'
        ]


class RoomDetailSerializer(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id', 'title', 'description', 'price_per_night', 'beds', 'bedrooms',
            'bathrooms', 'guests', 'category', 'wing', 'image_url', 'availability_status',
            'created_at', 'reservations'
        ]

    def get_reservations(self, obj):
        from reservations.serializers import ReservationSerializer
        # Assuming related_name is `reservation_set`
        reservations = obj.reservation_set.all()
        return ReservationSerializer(reservations, many=True, context=self.context).data
