from django.urls import path

from .consumers import ChatRoomConsumer

websocket_urlpatterns = [
    path("ws/messenger/chatroom/<str:chatroom__name>/", ChatRoomConsumer.as_asgi()),
]