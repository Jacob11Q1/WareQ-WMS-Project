from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with roles for access control.
    """

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("staff", "Staff"),
        ("viewer", "Viewer"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="viewer",
        help_text="Defines what permissions this user has in the system.",
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when the user was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update timestamp for this user.")

    def __str__(self):
        return f"{self.username} ({self.role})"

    # Helper methods
    def is_admin(self):
        return self.role == "admin"

    def is_manager(self):
        return self.role == "manager"

    def is_staff_user(self):
        return self.role == "staff"

    def is_viewer(self):
        return self.role == "viewer"
