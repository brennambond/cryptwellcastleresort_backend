from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserDetailSerializer, UserRegistrationSerializer
from .models import User
from rest_framework import status


@swagger_auto_schema(method='get', responses={200: UserDetailSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    """
    Retrieve details of the currently authenticated user.
    """
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserRegistrationSerializer, responses={201: UserDetailSerializer})
@api_view(['POST'])
def register_user(request):
    """
    Register a new user.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserDetailSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
