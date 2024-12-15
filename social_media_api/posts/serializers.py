from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers']  # Add any fields you want to expose

# Serializer for the Post model
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Show author's username
    comments = serializers.StringRelatedField(many=True, read_only=True)  # List of comments (optional)

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments')

# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Show author's username

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created_at', 'updated_at')
