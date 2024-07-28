from django.urls import path
from .views import PrivateChatroomListView, GroupChatroomListView, ChatroomMessagesView

urlpatterns = [
    path("private-chatrooms/", PrivateChatroomListView.as_view(), name="private-chatrooms"),
    path("group-chatrooms/", GroupChatroomListView.as_view(), name="private-chatrooms"),
    path("chatroom/<str:chatroom__name>/", ChatroomMessagesView.as_view(), name="chatroom-messages"),
]