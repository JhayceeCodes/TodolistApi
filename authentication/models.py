from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []
