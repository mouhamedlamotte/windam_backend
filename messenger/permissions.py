from rest_framework.permissions import BasePermission
from .models import ChatRoom


class IsGroupMember(BasePermission):
    def has_permission(self, request, view):
        try :
            if request.user not in ChatRoom.objects.get(name=view.kwargs['chatroom__name']).members.all():
                return False
        except ChatRoom.DoesNotExist:
            return False
        return super().has_permission(request, view)