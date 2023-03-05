from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
    ('superuser', 'superuser'),
)


class User(AbstractUser):
    bio = models.TextField(
            'Биография',
            blank=True,
        )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default='user',
    )

    def is_admin(self):
        if self.role == 'admin' or self.role == 'superuser':
            return True
        return False

    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False