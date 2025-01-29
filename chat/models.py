from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user1", "user2"]

    @staticmethod
    def get_or_create_room(user1, user2):
        # Ensure consistent room creation regardless of user order
        if user1.id > user2.id:
            user1, user2 = user2, user1
        room, created = ChatRoom.objects.get_or_create(user1=user1, user2=user2)
        return room


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
