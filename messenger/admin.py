from django.contrib import admin

from .models import ChatRoom, ChatroomMessage



admin.site.register(ChatRoom)
admin.site.register(ChatroomMessage)