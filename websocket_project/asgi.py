"""
ASGI config for websocket_project.

This module configures the ASGI application for both HTTP and WebSocket protocols.
It sets up the routing and middleware stack for handling different types of connections.

Protocol stack:
- HTTP: Standard Django application
- WebSocket: Channels application with authentication
"""

import os
import django

# Configure Django settings before importing other modules
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websocket_project.settings")
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from chat.routing import websocket_urlpatterns

# Configure the ASGI application
application = ProtocolTypeRouter(
    {
        # HTTP requests are handled by Django's standard ASGI application
        "http": get_asgi_application(),
        # WebSocket requests go through several layers:
        # 1. AllowedHostsOriginValidator: Ensures the request origin is allowed
        # 2. AuthMiddlewareStack: Handles authentication
        # 3. URLRouter: Routes to appropriate consumer based on URL
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
