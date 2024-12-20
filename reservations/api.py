from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Reservation
from .serializers import ReservationSerializer


@swagger_auto_schema(method='get', responses={200: ReservationSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_reservations(request):
    """
    Retrieve all reservations for the authenticated user.
    """
    reservations = Reservation.objects.filter(user=request.user)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=ReservationSerializer, responses={201: ReservationSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    """
    Create a new reservation for the authenticated user.
    """
    serializer = ReservationSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
