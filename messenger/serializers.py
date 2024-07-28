from .models import ChatRoom, ChatroomMessage
from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserAccountPubliqueSerializer


class PrivateChatroomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['pk','name', 'user', 'last_message', 'last_message_by']
    
    def get_user(self, obj):
        user = obj.members.exclude(pk=self.context['request'].user.pk)
        return UserAccountPubliqueSerializer(user, many=True).data if user else None


class GroupChatroomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    created_by = UserAccountPubliqueSerializer(read_only=True)
    members = UserAccountPubliqueSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = ['pk','name', 'created_by', 'last_message_by', 'last_message', 'group_name', 'members', 'created_at']
        
        
class ChatroomMessageSerializer(serializers.ModelSerializer):
    sender = UserAccountPubliqueSerializer(read_only=True)
    
    class Meta:
        model = ChatroomMessage
        fields = ['sender', 'type', 'file', 'content', 'seen', 'created_at']