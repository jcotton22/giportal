from django.contrib.auth.tokens import PasswordResetTokenGenerator

# ==============================
# Activation Token Generator
# ==============================

class ActivationTokenGenerator(PasswordResetTokenGenerator):
    """
        Email activation uses the same pattern as the password reset token
    """
    pass 

activation_token = ActivationTokenGenerator()

# ==============================
# Password Reset Token Generator
# ==============================

class PasswordResetTokenGeneratorCustom(PasswordResetTokenGenerator):
    pass

password_reset_token = PasswordResetTokenGeneratorCustom()

