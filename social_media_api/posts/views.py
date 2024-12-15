from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer  # Assuming you have a serializer for CustomUser
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post
from accounts.models import CustomUser  # Import your CustomUser model
from .serializers import PostSerializer  # Assuming you have a Post serializer

class UserFeedView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the current user
        user = request.user
        
        # Get the list of users that the current user is following
        following_users = user.following.all()

        # Filter posts that are written by the users the current user is following
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Serialize the posts
        serializer = PostSerializer(posts, many=True)

        # Return the serialized posts as the response
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch all users
        users = CustomUser.objects.all()  # Correct query for CustomUser model

        # Serialize the users using CustomUserSerializer
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['title', 'content']  # Allow searching by title or content
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Viewset for Comment model
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Authenticated users can create, edit, and delete; others can view

    def perform_create(self, serializer):
        post = serializer.validated_data['post']
        serializer.save(author=self.request.user, post=post)  # Automatically assign the logged-in user as the author

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsOwnerOrReadOnly()]
        return super().get_permissions()
