from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    """
    Custom User model that extends Django's default AbstractUser.
    We add a role field for access control.
    """

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('viewer', 'Viewer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer',
        help_text="Defines what permissions this user has in the system."
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when the user was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update timestamp for this user.")

    def __str__(self):
        return f"{self.username} ({self.role})"