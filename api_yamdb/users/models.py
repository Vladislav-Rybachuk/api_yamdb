from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(
            'Биография',
            blank=True,
        )
    role = models.CharField(
        max_length=10,
    )