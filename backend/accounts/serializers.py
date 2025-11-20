from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .tokens import activation_token, password_reset_token 
from .utils import send_activation_email, send_password_reset_email

User = get_user_model()

# ==============================
# REGISTRATION SERIALIZER
# ==============================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_email(self, value):
        """
            Check email domain is in allowed list
        """
        value = value.lower()
        if "@" not in value:
            raise serializers.ValidationError("Enter a valid email address")
        domain = value.split("@")[-1]
        allowed_domains = getattr(settings, "ALLOWED_EMAIL_DOMAINS", [])
        if allowed_domains and domain not in allowed_domains:
            raise serializers.ValidationError("Email domain is not allowed")
        return value
    
    def validate_password(self, value):
        """
            Use Django's build in password validators
        """
        validate_password(value)
        return value
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active=True
        user.is_email_verified=False
        user.save()

        #Send activation email
        send_activation_email(user)

        return user
    
# ==============================
# ACTIVATION SERIALIZER
# ==============================

class ActivateSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid activation link")
        
        if not activation_token.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired activation token")
        
        attrs["user"] = user
        return attrs
    
    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.is_email_verified = True
        user.save()

        return user
    
# ==============================
# CHANGE PASSWORD
# ==============================

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def save(self, **kwargs):
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user

# ==============================
# PASSWORD RESET
# ==============================

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower()
    
    def save(self, **kwargs):
        email = self.validated_data["email"]
        user = User.objects.filter(email=email, is_active=True).first()

        if user:
            send_password_reset_email(user)

        return {"detail" : "If an account with this email exists, a resent link has been sent."}
    

# ==============================
# PASSWORD RESET CONFIRMATION
# ==============================

class PasswordResetConfirmationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")
        new_password = attrs.get("new_password")

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link")
        
        if not password_reset_token.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired reset token")
        
        validate_password(new_password, user=user)
        attrs["user"] = user
        return attrs
    
    def save(self, **kwargs):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user

    
# ==============================
# EXTEND SIMPLE JWT SERIALIZER
# ==============================

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        Overrides SimpleJWTs login serializer to reject unverified users
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        
        #self.user is set by the parent class when auth succeeds
        if not self.user.is_email_verified:
            raise serializers.ValidationError("Please verify your email address before logging in")
        
        #Optionally include extra info in token response
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["is_email_verified"] = self.user.is_email_verified
        return data