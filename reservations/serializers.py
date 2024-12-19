from rest_framework import serializers
from .models import Reservation
from room.serializers import RoomSerializer


class ReservationSerializer(serializers.ModelSerializer):
    room_details = RoomSerializer(source="room", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "room",
            "room_details",
            "start_date",
            "end_date",
            "guests",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
