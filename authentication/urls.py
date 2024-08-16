from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import Me, SendOTP, VerifyOTP, RegisterUser

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('me/', Me.as_view(), name='me'),
    
    path('send-otp/', SendOTP.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('register/', RegisterUser.as_view(), name='register'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]