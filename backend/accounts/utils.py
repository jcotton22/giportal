from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes

from .tokens import activation_token

# ==============================
# Send activation email
# ==============================

def send_activation_email(user):
    """
        Build an activation link and send it to the user's email address
        Does not expose the user's password    
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = activation_token.make_token(user)

    # Frontend route like /activate?uid=...&token=..
    activation_link = f"{settings.ACTICATION_BASE_URL}/activate/?uid={uidb64}&token={token}"
    subject = "Please activate your giportal.ca account"
    message = (
        f"Hi {user.username}! \n\n"
        f"Welcome to giportal.ca!"
        f"Please click the link below to verify your email and activate your account \n\n"
        f"{activation_link}\n\n"
        f"Please ignore this email if you did not sign up for giportal.ca"
    )

    #Send
    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@giportal.ca"),
        [user.email],
        fail_silently=False
    )

# ==============================
# Send password reset email
# ==============================

from .tokens import password_reset_token

def send_password_reset_email(user):
    uidb4 = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)

    reset_link = f"{settings.ACTIVATION_BASE_URL}/reset-password?uid={uidb4}&token={token}"

    subject = "Reset your giportal.ca password"
    message = (
        f"Hi {user.username},\n\n"
        f"We've receoved your password request to giportal.ca\n\n"
        f"You can reset your password with the link below:\n\n"
        f"{reset_link}\n\n"
        "Please ignore this email if you didn't request this \n\n"
        "Sincerely,\n\n"
        "The GI Portal team"
    )

    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", "no-replay@giportal.ca"),
        [user.email],
        fail_silently=False
    )