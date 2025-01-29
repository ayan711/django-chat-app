"""
WebSocket Consumer for handling real-time chat functionality.

This module contains the AsyncWebsocketConsumer class that handles:
- WebSocket connections
- Message receiving and sending
- Database operations for message persistence
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Handles WebSocket connections and message routing for the chat application.

    Attributes:
        room_id (str): The ID of the chat room
        room_group_name (str): The channel layer group name for the room
    """

    async def connect(self):
        """
        Handles new WebSocket connections.

        - Extracts room_id from URL route
        - Creates a unique group name for the room
        - Adds the channel to the room group
        - Accepts the WebSocket connection
        """
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.

        Args:
            close_code: The code indicating why the connection was closed
        """
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handles incoming messages from WebSocket.

        Args:
            text_data (str): JSON string containing the message data

        Flow:
            1. Parses the JSON message
            2. Extracts message content and user ID
            3. Saves message to database
            4. Broadcasts message to room group
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = self.scope["user"].id

        # Save message to database
        await self.save_message(message, user_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "user_id": user_id},
        )

    async def chat_message(self, event):
        """
        Handles sending messages to WebSocket.

        Args:
            event (dict): Contains message data to be sent
        """
        message = event["message"]
        user_id = event["user_id"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user_id": user_id}))

    @database_sync_to_async
    def save_message(self, message, user_id):
        """
        Saves a message to the database.

        Args:
            message (str): The message content
            user_id (int): The ID of the message sender

        Note:
            This method is decorated with database_sync_to_async to make it
            safe to call from asynchronous context.
        """
        user = User.objects.get(id=user_id)
        room = ChatRoom.objects.get(id=self.room_id)
        Message.objects.create(content=message, sender=user, room=room)
