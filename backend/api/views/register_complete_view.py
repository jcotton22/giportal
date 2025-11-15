# api/views/register_complete_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from api.serializers import RegisterCompleteSerializer

class RegisterCompleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = RegisterCompleteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"detail": "Account activated."}, status=status.HTTP_200_OK)
