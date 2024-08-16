from rest_framework import generics, permissions

from .models import User

from .serializers import UserAccountSerializer, UpdateUserAccountSerializer

from windam_backend.permissions import IsOwner, IsSuperUser


class ListUserAccountView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    

class RetrieveUpdateDestroyAccountView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserAccountSerializer

    def get_permissions(self):
        try:
            queryset= User.objects.get(pk=self.request.user.pk)
            if queryset.pk == self.kwargs.get('pk'):
                return [permissions.IsAuthenticated()]
            else:
                return [IsSuperUser()]
        except User.DoesNotExist:
            return [IsSuperUser()]
    
class AddUserAccountView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    
    