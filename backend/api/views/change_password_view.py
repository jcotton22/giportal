from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import (
    ChangePasswordSerializer,
)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = ChangePasswordSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"detail": "Password changed successfully."})