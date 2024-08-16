from django.db import models
import shortuuid
from accounts.models import User

# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True, default=shortuuid.uuid)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms_created_by')
    group_name = models.CharField(max_length=255, blank=True)
    private = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='chatrooms_members', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message = models.JSONField(null=True, blank=True)
    last_message_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='last_message_by', null=True, blank=True)
    def __str__(self):
        if self.private:
            try : 
                return  f"discussion : {self.name} entre {self.members.all()[0].username} et {self.members.all()[1].username}"
            except :
                return  f"discussion : {self.name} de {self.members.all()[0].username}"
        return f"Groupe : {self.group_name}"
    
    
class ChatroomMessage(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=[('text', 'text'), ('image', 'image'), ('caption', 'caption'),('code', 'code'), ('audio', 'audio')])
    file = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.sender.username} : {self.content}"
    
    class Meta:
        ordering = ['-created_at']