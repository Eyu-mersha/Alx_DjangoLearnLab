from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.permissions import permissions.IsAuthenticated
# Follow user
@api_view(['POST'])
def follow_user(request, user_id):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Ensure a user doesn't follow themselves
    if user_to_follow == request.user:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.following.add(user_to_follow)  # Add to following
    return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)

# Unfollow user
@api_view(['POST'])
def unfollow_user(request, user_id):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    # Ensure a user doesn't unfollow themselves
    if user_to_unfollow == request.user:
        return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.remove(user_to_unfollow)  # Remove from following
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
