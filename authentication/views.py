from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserAccountSerializer
from django.core.mail import send_mail

from rest_framework import serializers, generics

import pyotp

from constants import OTP_SECRET_KEY


class Me(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserAccountSerializer(request.user).data)
    
class SendMailSerializer(serializers.Serializer):
    email = serializers.EmailField()
class VeryfyMailSerializer(serializers.Serializer):
    otp_code = serializers.CharField()

class SendOTP(generics.CreateAPIView):
    permission_classes = []
    serializer_class = SendMailSerializer
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"email": "This field is required dddd."}, status=400)
        

        hotp = pyotp.HOTP(OTP_SECRET_KEY)
        otp_code = hotp.at(0)
        

        print("Your HMAC-based OTP:", otp_code)

        try :
            send_mail(
                "Subject here",
                f"Here is your OTP: {otp_code}",
                "mouhamedlamotte.dev@gmail.com",
                [email],
            )
        except Exception as e:
            print(e)
            return Response({"detail": "Something went wrong"}, status=400)

        response = {
            'otp_code' : otp_code,
            'message' : 'OTP sent to your email.'         
        }
        
        return Response(response)
    
class VerifyOTP(generics.CreateAPIView):
    permission_classes = []
    serializer_class = VeryfyMailSerializer
    def post(self, request):
        otp_code = request.data.get('otp_code')
        if not otp_code:
            return Response({"otp_code": "This field is required."}, status=400)
        hotp = pyotp.HOTP(OTP_SECRET_KEY)
        if hotp.verify(otp_code, 0):
            return Response({"detail": "OTP is valid."}, status=200)
        else:
            return Response({"detail": "OTP is invalid."}, status=400)
        
class RegisterUser(generics.CreateAPIView):
    permission_classes = []
    serializer_class = UserAccountSerializer