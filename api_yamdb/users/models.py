from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
    ('superuser', 'superuser'),
)


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    SUPERUSER = 'superuser'

    ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
        (SUPERUSER, 'superuser'),
    ]

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
