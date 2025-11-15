from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from api.utils.is_email_allowed import is_email_allowed

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class RegisterStartSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        email = value.strip().lower()
        if not is_email_allowed(email):
            allowed = ", ".join(getattr(settings, "ALLOWED_EMAIL_DOMAINS", []))
            raise serializers.ValidationError(
                f"Registration is restricted to {allowed} domains."
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def create(self, validated_data):
        email = validated_data["email"]
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'username': email, 'is_active': False}  # <-- use full email
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        base = getattr(settings, "ACTIVATION_BASE_URL", "")
        link = f"{base}?uid={uid}&token={token}"

        # Dev breadcrumbs — these print in the **runserver** terminal
        print("[RegisterStart] creating for:", email)
        print("[RegisterStart] activation link:", link)

        send_mail(
            subject="Activate your account",
            message=f"Please click the following link to activate your account:\n\n{link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,  # <-- make failures visible
        )
        return {"email": email}
