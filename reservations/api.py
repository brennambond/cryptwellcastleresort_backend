# Updated `reservations/api.py`
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Reservation
from room.models import Room
from .serializers import ReservationSerializer
from django.db.models import Q


def validate_reservation_dates(start_date, end_date):
    if start_date >= end_date:
        return False, "End date must be after start date."
    return True, None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_reservations(request):
    reservations = Reservation.objects.filter(
        user=request.user).order_by('-created_at')
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    serializer = ReservationSerializer(data=request.data)

    if serializer.is_valid():
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        is_valid, error_message = validate_reservation_dates(
            start_date, end_date)

        if not is_valid:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        existing_reservations = Reservation.objects.filter(
            room=room,
        ).filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
        )

        if existing_reservations.exists():
            return Response({"error": "Room is already reserved for the selected dates."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user, room=room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
