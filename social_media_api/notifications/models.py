from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL  # Use the custom user model

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)  # The user receiving the notification
    actor = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)  # The user performing the action
    verb = models.CharField(max_length=255)  # Describes the action (e.g., "liked", "followed", etc.)
    
    # GenericForeignKey allows us to link to any model (Post, Comment, etc.)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # The content type (Post, Comment, etc.)
    target_object_id = models.PositiveIntegerField()  # The ID of the target object (Post, Comment, etc.)
    target = GenericForeignKey('target_content_type', 'target_object_id')  # The actual object being targeted (Post, Comment, etc.)
    
    timestamp = models.DateTimeField(auto_now_add=True)  # The time when the notification was created
    read = models.BooleanField(default=False)  # To mark the notification as read or unread
    
    class Meta:
        ordering = ['-timestamp']  # Order notifications by timestamp (most recent first)

    def __str__(self):
        return f"{self.actor.username} {self.verb} {self.target}"

    def mark_as_read(self):
        """Mark notification as read."""
        self.read = True
        self.save()
