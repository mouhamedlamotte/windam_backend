from rest_framework import generics, permissions

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
        return ChatRoom.objects.filter(members=self.request.user)
    
class ChatroomMessagesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]
    serializer_class = ChatroomMessageSerializer
    lookup_field = 'chatroom__name'
    
    def get_queryset(self):
        chatroom = ChatRoom.objects.filter(name=self.kwargs['chatroom__name']).first()
        if chatroom and self.request.user in chatroom.members.all():
            return ChatroomMessage.objects.filter(chatroom__name=self.kwargs['chatroom__name'])
        return ChatroomMessage.objects.none()