"""
View handlers for the chat application.

This module contains the view functions that handle HTTP requests for:
- User authentication
- Chat room creation and access
- User list display
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from django.db.models import Q


@login_required
def index(request):
    """
    Displays the list of available users to chat with.

    Args:
        request: The HTTP request object

    Returns:
        Rendered template with list of users excluding the current user
    """
    users = User.objects.exclude(id=request.user.id)
    return render(request, "chat/index.html", {"users": users})


@login_required
def room(request, user_id):
    """
    Handles chat room display and creation.

    Args:
        request: The HTTP request object
        user_id: The ID of the user to chat with

    Returns:
        Rendered chat room template with room context

    Flow:
        1. Gets or creates chat room for the two users
        2. Loads existing messages
        3. Renders template with room and message context
    """
    other_user = User.objects.get(id=user_id)
    chat_room = ChatRoom.get_or_create_room(request.user, other_user)
    messages = Message.objects.filter(room=chat_room)
    return render(
        request,
        "chat/room.html",
        {"other_user": other_user, "room_id": chat_room.id, "messages": messages},
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Get the next URL or default to index
            next_url = request.GET.get("next", "index")
            # Prevent redirect loops by checking if next_url contains 'login'
            if "login" in next_url:
                return redirect("index")
            return redirect(next_url)
    return render(request, "chat/login.html")
