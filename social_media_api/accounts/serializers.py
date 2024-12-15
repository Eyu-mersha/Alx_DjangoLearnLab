from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    # Meta class to define fields and how the password should be handled
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create user using create_user to ensure password is hashed
        user = get_user_model().objects.create_user(**validated_data)

        # Create a token for the user after creation
        token = Token.objects.create(user=user)

        # Add token to the user instance's representation (to be returned as part of the response)
        validated_data['token'] = token.key

        return user

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()