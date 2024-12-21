from rest_framework import serializers
from .models import Reservation
from room.serializers import RoomSerializer


class ReservationSerializer(serializers.ModelSerializer):
    # room_details = RoomSerializer(source='room', read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    room_details = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'check_in', 'check_out', 'guests', 'room', 'room_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_room_details(self, obj):
        return {
            "id": obj.room.id,
            "title": obj.room.title,
            "price_per_night": obj.room.price_per_night,
            "image_url": obj.room.image_url.url if obj.room.image_url else None,
            "beds": obj.room.beds,
            "bedrooms": obj.room.bedrooms,
            "bathrooms": obj.room.bathrooms,
            "guests": obj.room.guests
        }

# In urls.py, you are using int:pk for some reason instead of uuid:reservation_id
# In admin.py, you are missing user, id, and list_filter and search_fields.
