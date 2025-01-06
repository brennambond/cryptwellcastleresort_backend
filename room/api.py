from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Room, Wing
from reservations.models import Reservation  # Corrected import
from reservations.serializers import ReservationSerializer
from .serializers import RoomSerializer, WingSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q, F


@api_view(['GET'])
def list_rooms(request):

    rooms = Room.objects.annotate(
        wing_priority=F('wing__name')
    ).order_by(
        '' 'wing_priority',
        'price_per_night',
        'title'
    )

    # Apply filtering
    guests = request.query_params.get('guests')
    beds = request.query_params.get('beds')
    bedrooms = request.query_params.get('bedrooms')
    bathrooms = request.query_params.get('bathrooms')
    check_in = request.query_params.get('checkIn')
    check_out = request.query_params.get('checkOut')

    if guests:
        rooms = rooms.filter(guests__gte=int(guests))
    if beds:
        rooms = rooms.filter(beds__gte=int(beds))
    if bedrooms:
        rooms = rooms.filter(bedrooms__gte=int(bedrooms))
    if bathrooms:
        rooms = rooms.filter(bathrooms__gte=int(bathrooms))

    # Check for availability based on reservations
    if check_in and check_out:
        reservations = Reservation.objects.filter(
            Q(check_in__lte=check_out) & Q(check_out__gte=check_in)
        ).values_list('room_id', flat=True)
        rooms = rooms.exclude(id__in=reservations)

    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    serializer = RoomSerializer(room)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
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
