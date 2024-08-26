from channels.generic.websocket import WebsocketConsumer
from messenger.models import ChatRoom, ChatroomMessage
from django.shortcuts import get_object_or_404
from .serializers import ChatroomMessageSerializer

from asgiref.sync import async_to_sync

import json

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom__name']
        self.chatroom = get_object_or_404(ChatRoom, name=self.chatroom_name)
        self.channel_layer.group_add(
            self.chatroom_name, self.channel_name
        )
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        self.accept()

    def receive(self, text_data =None, bytes_data=None):
        text_data_json = json.loads(text_data)
        sender = self.user
        msg_type = text_data_json.get('type', 'text')
        content = text_data_json.get('content', None)
        message = ChatroomMessage.objects.create(
            sender=sender,
            type= msg_type,
            content=content,
            chatroom = self.chatroom
        )
        self.update_last_message(message)
        event = {
            'type': 'message_handler',
            'message_pk' : message.pk
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
    def message_handler(self, event):
        message_pk = event['message_pk']
        message = ChatroomMessage.objects.get(pk=message_pk)
        serialized = ChatroomMessageSerializer(message).data
        self.send(text_data=json.dumps({
            'message': serialized
        }))
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )
    def update_last_message(self, message):
        self.chatroom.last_message = {
            'content': message.content,
            'created_at': message.created_at.isoformat(),
            'type': message.type
        }
        self.chatroom.last_message_by = message.sender
        self.chatroom.save()