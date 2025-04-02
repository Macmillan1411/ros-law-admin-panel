from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    EDITOR = "editor"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

    ROLE_CHOICES = [
        (EDITOR, "Editor"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Admin"),
        (SUPERADMIN, "Super Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EDITOR)
    patronymic = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Отчество"
    )
    position = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Должность"
    )
    approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(blank=True, null=True)

    def is_content_admin(self):
        return self.role in [self.ADMIN, self.SUPERADMIN]

    def is_moderator(self):
        return self.role in [self.MODERATOR, self.ADMIN, self.SUPERADMIN]

    def is_editor(self):
        return self.role in [self.EDITOR, self.ADMIN, self.SUPERADMIN]

    def get_full_name(self):
        """
        Return the first_name plus the last_name plus the patronymic, with a space in between.
        """
        full_name = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name.strip()
