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

# Helper function


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
        logger.info(
            f"Fetched reservations for user {request.user}: {reservations}")
        serializer = ReservationSerializer(reservations, many=True)
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
        logger.info(
            f"Fetched reservation {reservation_id} for user {request.user}.")
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching reservation: {e}", exc_info=True)
        return Response({"error": "An error occurred while fetching the reservation."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    try:
        room_id = request.data.get('room_id')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')
        guests = request.data.get('guests')
        total_price = request.data.get('total_price')

        if not all([room_id, check_in, check_out, guests, total_price]):
            return Response({'error': 'Missing fields in request.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

        reservation = Reservation.objects.create(
            user=request.user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            total_price=total_price
        )

        serializer = ReservationSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation Errors:", serializer.errors)
            return Response({'error': 'Missing fields in request.', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': 'An error occurred during reservation creation.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_reservation(request, reservation_id):
    try:
        logger.info(f"Updating reservation {reservation_id}.")
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
        serializer = ReservationSerializer(reservation)
        logger.info(f"Reservation updated successfully: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error updating reservation: {e}", exc_info=True)
        return Response({"error": "An error occurred while updating the reservation."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reservation(request, reservation_id):
    try:
        reservation = get_object_or_404(
            Reservation, id=reservation_id, user=request.user
        )
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": "An error occurred while deleting the reservation."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
