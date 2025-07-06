from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Reservation
from .serializers import ReservationSerializer
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from room.models import Room
import logging

logger = logging.getLogger(__name__)


def validate_dates(check_in, check_out):
    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')

        if check_in_date >= check_out_date:
            raise ValidationError(
                "Check-in date must be before check-out date.")

        if check_in_date < datetime.now():
            raise ValidationError("Check-in date cannot be in the past.")
    except ValueError as e:
        raise ValidationError(f"Invalid date format: {e}")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_reservations(request):
    try:
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(
            reservations, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching reservations: {e}", exc_info=True)
        return Response({"error": "An error occurred while fetching reservations."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reservation(request, reservation_id):
    try:
        reservation = get_object_or_404(
            Reservation, id=reservation_id, user=request.user)
        serializer = ReservationSerializer(
            reservation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching reservation: {e}", exc_info=True)
        return Response({"error": "An error occurred while fetching the reservation."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    try:
        data = request.data.copy()
        room_id = data.get('room')

        if not room_id:
            return Response({'error': 'Missing room ID.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

        data['user'] = request.user.id
        data['room'] = room.id

        validate_dates(data.get('check_in'), data.get('check_out'))

        serializer = ReservationSerializer(
            data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, room=room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"Validation failed: {serializer.errors}")
            return Response({'error': 'Validation failed.', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error creating reservation: {e}", exc_info=True)
        return Response({'error': 'An error occurred during reservation creation.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_reservation(request, reservation_id):
    try:
        reservation = get_object_or_404(
            Reservation, id=reservation_id, user=request.user)
        data = request.data

        reservation.check_in = data.get('check_in', reservation.check_in)
        reservation.check_out = data.get('check_out', reservation.check_out)
        reservation.guests = data.get('guests', reservation.guests)
        reservation.total_price = data.get(
            'total_price', reservation.total_price)

        validate_dates(reservation.check_in, reservation.check_out)

        reservation.save()
        serializer = ReservationSerializer(
            reservation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error updating reservation: {e}", exc_info=True)
        return Response({"error": "An error occurred while updating the reservation."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reservation(request, reservation_id):
    try:
        reservation = get_object_or_404(
            Reservation, id=reservation_id, user=request.user)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error deleting reservation: {e}", exc_info=True)
        return Response({"error": "An error occurred while deleting the reservation."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
