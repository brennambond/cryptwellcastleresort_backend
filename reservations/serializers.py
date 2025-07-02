from rest_framework import serializers
from .models import Reservation
from room.serializers import WingSerializer
from datetime import datetime


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    room = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'check_in', 'check_out', 'guests', 'total_price', 'room', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_room(self, obj):
        try:
            # Serialize the wing object
            wing_data = WingSerializer(obj.room.wing).data
            return {
                "id": obj.room.id,
                "title": obj.room.title,
                "price_per_night": obj.room.price_per_night,
                "image": obj.room.image,
                "beds": obj.room.beds,
                "bedrooms": obj.room.bedrooms,
                "bathrooms": obj.room.bathrooms,
                "guests": obj.room.guests,
                "wing": wing_data,  # Include serialized wing
            }
        except AttributeError as e:
            raise serializers.ValidationError(
                f"Error retrieving room data: {e}")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['check_in'] = (
            instance.check_in.strftime('%Y-%m-%d')
            if isinstance(instance.check_in, datetime)
            else instance.check_in
        )
        rep['check_out'] = (
            instance.check_out.strftime('%Y-%m-%d')
            if isinstance(instance.check_out, datetime)
            else instance.check_out
        )
        return rep
