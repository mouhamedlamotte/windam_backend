from typing import Any
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import ChatRoom, ChatroomMessage
from .serializers import PrivateChatroomSerializer, GroupChatroomSerializer, ChatroomMessageSerializer


# Create your views here.

from rest_framework import generics, permissions

from .models import ChatRoom
from .serializers import PrivateChatroomSerializer


from .permissions import IsGroupMember

class PrivateChatroomListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PrivateChatroomSerializer
    
    def get_queryset(self):
        return ChatRoom.objects.filter(members=self.request.user, private=True)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class GroupChatroomListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupChatroomSerializer
    
    def get_queryset(self):
        return ChatRoom.objects.filter(members=self.request.user, private=False)
    
from rest_framework.response import Response
from rest_framework import generics, permissions

class ChatroomMessagesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]
    serializer_class = ChatroomMessageSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    
    def get_queryset(self):
        chatroom_name = self.kwargs.get('chatroom__name')
        chatroom = ChatRoom.objects.filter(name=chatroom_name).first()
        if chatroom and self.request.user in chatroom.members.all():
            return ChatroomMessage.objects.filter(chatroom=chatroom).order_by('created_at')
        return ChatroomMessage.objects.none()
    

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        chatroom_name = self.kwargs.get('chatroom__name')
        chatroom = ChatRoom.objects.filter(name=chatroom_name).first()
        chats = response.data
        
        if chatroom:
            chatroom_data = GroupChatroomSerializer(chatroom).data
            chatroom_data["private"] = chatroom.private
        else:
            chatroom_data = None
        return Response({
            'chats': chats,
            'chatroom': chatroom_data
        })