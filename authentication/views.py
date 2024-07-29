from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserAccountSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserAccountSerializer(request.user).data)
