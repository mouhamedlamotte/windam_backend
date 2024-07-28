from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsOwner(permissions.BasePermission):
    
    def __init__(self, obj = None) -> None:
        self.obj = obj
        

    def has_object_permission(self, request, view, obj):
        if self.obj != None:
            obj = self.obj
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.owner == request.user
        else:
            return False