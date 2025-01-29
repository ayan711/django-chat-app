from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/<int:user_id>/", views.room, name="room"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="chat/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
]
