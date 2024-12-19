from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserDetailSerializer, UserRegistrationSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import User


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserDetailSerializer(user, many=False)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    serializer = UserDetailSerializer(user)  # Serialize the user object
    return Response(serializer.data)  # Return serialized user data


@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=email, password=password)

    if user is not None:
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return tokens and user_id
        return Response({
            "message": "Login successful",
            "user_id": str(user.id),
            "access": access_token,
            "refresh": str(refresh),
        })
    else:
        return Response({"detail": "Invalid credentials"}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout the user by clearing the session and blacklisting the refresh token if provided.
    """
    logout(request)  # Clears the session

    # Blacklist refresh token if provided
    refresh_token = request.data.get("refresh")
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    return Response({"message": "Successfully logged out"}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"detail": "User registered successfully.", "user_id": user.id},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
