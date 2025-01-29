"""
WebSocket URL configuration for the chat application.

This module defines the WebSocket URL patterns that map to consumer classes.
The patterns use regex to capture room IDs from the WebSocket URL.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # URL pattern for chat room WebSocket connections
    # Format: ws://domain/ws/chat/<room_id>/
    re_path(r"^ws/chat/(?P<room_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
]
