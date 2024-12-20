from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    reservation = get_object_or_404(
        Reservation, id=reservation_id, user=request.user)
    serializer = ReservationSerializer(
        reservation, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    return Response({"detail": "Reservation deleted."}, status=status.HTTP_204_NO_CONTENT)
