from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import RegisterStartSerializer

class RegisterStartView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = RegisterStartSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        out = ser.save()  # will send the email
        print("[RegisterStartView] sent activation for:", out["email"])  # <-- debug
        return Response({"detail": "Activation email sent."}, status=status.HTTP_201_CREATED)
