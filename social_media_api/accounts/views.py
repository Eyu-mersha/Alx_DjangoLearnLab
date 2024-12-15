from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.permissions import IsAuthenticated
# Follow user
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        
        # Ensure the user cannot follow themselves
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add the user to the following list
        request.user.following.add(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        
        # Ensure the user cannot unfollow themselves
        if user_to_unfollow == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove the user from the following list
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Handle user registration
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # This will create the user and also generate a token
            return Response({
                'user': serializer.data  # Send back user data along with token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
