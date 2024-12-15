from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Post
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)  # User receiving the notification
    actor = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)  # User performing the action
    verb = models.CharField(max_length=255)  # Describes the action (e.g., "liked", "followed", etc.)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # The content type of the target (Post, Comment, etc.)
    target_object_id = models.PositiveIntegerField()  # ID of the target object (Post, Comment, etc.)
    target = GenericForeignKey('target_content_type', 'target_object_id')  # Generic relation to the target object (Post, Comment, etc.)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # To mark notifications as read

    def __str__(self):
        return f"{self.actor.username} {self.verb} {self.target}"

    def mark_as_read(self):
        self.read = True
        self.save()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who liked the post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # The post that was liked
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensures a user can only like a post once

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


# Post model to store user posts
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Comment model to store comments on posts
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

# Create your models here.
