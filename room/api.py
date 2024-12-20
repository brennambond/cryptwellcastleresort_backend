from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Wing, Room
from .serializers import WingSerializer, RoomSerializer


@swagger_auto_schema(method='get', responses={200: WingSerializer(many=True)})
@api_view(['GET'])
@permission_classes([AllowAny])
def list_wings(request):
    """
    Retrieve a list of all wings.
    """
    wings = Wing.objects.all()
    serializer = WingSerializer(wings, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: RoomSerializer(many=True)})
@api_view(['GET'])
@permission_classes([AllowAny])
def list_rooms(request):
    """
    Retrieve a list of all rooms.
    """
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)
