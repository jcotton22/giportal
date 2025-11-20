from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
        Custom user model
        Inherits username, password, email from AbstractUser
        Adds an is_email_verified flag that can be flipped after activation
    """

    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username