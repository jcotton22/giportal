from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class AllowSignupEmail(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.email
    
class AllowedSignupDomain(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.domain
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    must_change_password = models.BooleanField(default=True)
    def __str__(self):
        return f"Profile of {self.user.username}"