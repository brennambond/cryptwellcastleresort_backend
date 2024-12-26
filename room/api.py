from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Room, Wing
from reservations.models import Reservation  # Corrected import
from reservations.serializers import ReservationSerializer
from .serializers import RoomSerializer, WingSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def list_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    serializer = RoomSerializer(room)
    return Response(serializer.data)


@api_view(['GET'])
def list_wings(request):
    wings = Wing.objects.all()
    serializer = WingSerializer(wings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_wing_detail(request, wing_id):
    wing = get_object_or_404(Wing, id=wing_id)
    serializer = WingSerializer(wing)
    return Response(serializer.data)


@api_view(['GET'])
def get_room_reservations(request, room_id):
    """
    Get all reservations for a specific room.
    """
    room = get_object_or_404(Room, id=room_id)
    reservations = Reservation.objects.filter(room=room)
    data = [
        {
            "check_in": reservation.check_in,
            "check_out": reservation.check_out,
        }
        for reservation in reservations
    ]
    return Response(data, status=status.HTTP_200_OK)
