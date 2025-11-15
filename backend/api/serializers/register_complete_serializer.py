# api/serializers/register_complete_serializer.py
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class RegisterCompleteSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    # accept either 'password' or 'new_password'
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    new_password = serializers.CharField(write_only=True, required=False, min_length=8)

    def validate(self, data):
        pw = data.get("password") or data.get("new_password")
        if not pw:
            raise serializers.ValidationError({"password": "This field is required."})
        data["password"] = pw  # normalize
        return data

    def create(self, validated):
        uid = validated["uid"]
        token = validated["token"]
        password = validated["password"]

        user_id = force_str(urlsafe_base64_decode(uid))
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"uid": "Invalid activation link."})

        if not token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "Activation token is invalid or expired."})

        user.set_password(password)
        user.is_active = True
        user.save()
        return {"email": user.email}
