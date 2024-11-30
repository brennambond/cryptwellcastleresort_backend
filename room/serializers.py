from rest_framework import serializers

from .models import Room, Reservation, Wing, Category

from useraccount.serializers import UserDetailSerializer


class RoomsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
            'wing',
            'beds',
            'bedrooms',
            'bathrooms',
            'category',
            'guests',
        )


class WingsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wing
        fields = (
            'id', 'name', 'image_url', 'description'
        )


class RoomsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id',
            'title',
            'description',
            'price_per_night',
            'image_url',
            'beds',
            'bedrooms',
            'bathrooms',
            'category',
            'wing',
            'guests',
        )


class ReservationsListSerializer(serializers.ModelSerializer):
    room = RoomsListSerializer(read_only=True, many=False)

    class Meta:
        model = Reservation
        fields = (
            'id', 'start_date', 'end_date', 'number_of_nights', 'total_price', 'room', 'guests'
        )


class WingsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wing
        fields = (
            'id', 'name', 'image_url', 'description'
        )


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'description'
        )
