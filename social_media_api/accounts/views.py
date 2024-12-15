from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserSerializer, AuthTokenSerializer


# User Registration View
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Handle user registration
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # This will use the create method in UserSerializer
            token = Token.objects.create(user=user)  # Generate token after creating user
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login View (Token Retrieval)
class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            # Authenticate user using provided credentials
            user = authenticate(username=serializer.validated_data['username'], 
                                password=serializer.validated_data['password'])
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)  # Get or create a token
                return Response({'token': token.key})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
