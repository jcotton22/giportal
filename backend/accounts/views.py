from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    RegisterSerializer, 
    ActivateSerializer, 
    CustomTokenObtainPairSerializer, 
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmationSerializer,
)

# ==============================
# Register View
# ==============================

class RegisterView(generics.CreateAPIView):
    """
        POST /api/auth/register/
        Body: { "username": "...", "email": "...", "password": "..." }
    """

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Registration successful. Check your email to activate your account."},
            status=status.HTTP_201_CREATED,
        )

# ==============================
# Activate View
# ==============================

class ActivateView(APIView):
    """
        POST /api/auth/activate/
        Body: { "uid": "...", "token": "..." 
    """

    def post(self, request, *args, **kwargs):
        serializer = ActivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)
    

# ==============================
# Change password
# ==============================

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data = request.data,
            context={"request":request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail" : "Password changed successfully!"},
            status = status.HTTP_200_OK,
        )
    

# ==============================
# Password Resest
# ==============================

class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "If an account with this email exists, a reset link has been sent."},
            status = status.HTTP_200_OK
        )
    
# ==============================
# Password reset confirmation
# ==============================

class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password has been reset successfully."},
            status = status.HTTP_200_OK
        )
    
# ==============================
# Token Obtain pair view
# ==============================

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
