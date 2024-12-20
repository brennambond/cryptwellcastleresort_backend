from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework import status
from .serializers import UserDetailSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate, get_user_model
from .models import User
from rest_framework_simplejwt.exceptions import TokenError


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    """
    Retrieve details of the currently authenticated user.
    """
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)


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


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Authenticate the user and return a JWT token.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        return Response({"error": "Please provide both email and password."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Retrieve the current authenticated user's details.
    """
    user = request.user
    data = {
        "id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
    }
    return Response(data, status=status.HTTP_200_OK)
