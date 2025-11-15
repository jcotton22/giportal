# api/utils.py  (adjust path to your app)
from django.conf import settings

def is_email_allowed(email: str) -> bool:
    """
    Returns True if the email's domain matches exactly one of ALLOWED_EMAIL_DOMAINS.
    Normalizes case and trims whitespace/trailing dots.
    """
    if not email or "@" not in email:
        return False

    email = email.strip().lower()
    # Split once from right in case someone sneaks a second '@'
    _, domain = email.rsplit("@", 1)

    domain = domain.strip().strip(".")
    allowed = [d.strip().lower().strip(".") for d in getattr(settings, "ALLOWED_EMAIL_DOMAINS", [])]
    return domain in allowed
