from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from room.models import Room


def validate_dates(check_in, check_out):
    """
    Validates that check_in and check_out are valid and logically correct.
    """
    from datetime import datetime

    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        if check_in_date >= check_out_date:
            raise ValueError("Check-out date must be after check-in date.")
    except ValueError as e:
        raise ValueError(f"Invalid date format or logic: {e}")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_reservation(request):
    """
    Create a new reservation for a user.
    """
    data = request.data
    room_id = data.get('room')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    guests = data.get('guests', 1)
    total_price = data.get('total_price', 0.00)

    try:
        # Validate required fields
        if not all([check_in, check_out, room_id, total_price]) or int(guests) <= 0:
            return Response({"error": "Missing or invalid required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate dates
        validate_dates(check_in, check_out)

        # Fetch the room
        room = get_object_or_404(Room, id=room_id)

        # Create the reservation
        try:
            reservation = Reservation.objects.create(
                user=request.user,
                room=room,
                check_in=check_in,
                check_out=check_out,
                guests=guests,
                total_price=total_price,
            )
        except IntegrityError:
            return Response({"error": "A reservation already exists for this room and date range."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the reservation
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error: {e}")
        return Response({"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation, id=reservation_id, user=request.user)
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_reservation(request, reservation_id):
    try:
        reservation = get_object_or_404(
            Reservation, pk=reservation_id, user=request.user)
        data = request.data

        check_in = data.get('check_in', reservation.check_in)
        check_out = data.get('check_out', reservation.check_out)
        guests = data.get('guests', reservation.guests)
        room_id = data.get('room', reservation.room.id)

        validate_dates(check_in, check_out)

        room = get_object_or_404(Room, pk=room_id)
        reservation.room = room
        reservation.check_in = check_in
        reservation.check_out = check_out
        reservation.guests = guests
        reservation.save()

        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reservation(request, reservation_id):
    try:
        reservation = get_object_or_404(
            Reservation, pk=reservation_id, user=request.user)
        reservation.delete()
        return Response({"message": "Reservation deleted successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
