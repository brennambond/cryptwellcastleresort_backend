from rest_framework import serializers
from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name',
                  'last_name', 'is_staff', 'is_active')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            # Default to empty string if not provided
            first_name=validated_data.get('first_name', ''),
            # Default to empty string if not provided
            last_name=validated_data.get('last_name', '')
        )
        return user
