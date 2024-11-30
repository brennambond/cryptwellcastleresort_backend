from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import User
from .serializers import UserDetailSerializer

from room.serializers import ReservationsListSerializer


@api_view(['GET'])
def reservations_list(request):
    reservations = request.user.reservations.all()
    serializer = ReservationsListSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)
