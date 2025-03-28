from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    EDITOR = 'editor'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'

    ROLE_CHOICES = [
        (EDITOR, 'Editor'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
        (SUPERADMIN, 'Super Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EDITOR)

    def is_content_admin(self):
        return self.role in [self.ADMIN, self.SUPERADMIN]

    def is_moderator(self):
        return self.role in [self.MODERATOR, self.ADMIN, self.SUPERADMIN]

    def is_editor(self):
        return self.role in [self.EDITOR, self.ADMIN, self.SUPERADMIN]