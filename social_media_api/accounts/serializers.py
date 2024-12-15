from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Handle password hashing using create_user
        user = Token.objects.create_user(**validated_data)
        return user

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()