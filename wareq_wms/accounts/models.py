from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Company(models.Model):
    """
    Company model for multi-tenancy.
    Each company has its own subscription plan and users.
    """
    PLAN_CHOICES = (
        ("FREE", "Free"),
        ("PRO", "Pro"),
        ("ENTERPRISE", "Enterprise"),
    )

    name = models.CharField(max_length=255, unique=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="FREE")
    subscription_status = models.CharField(
        max_length=20,
        default="ACTIVE",
        help_text="ACTIVE, TRIAL, EXPIRED"
    )
    trial_end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_trial_active(self):
        return self.trial_end and self.trial_end >= timezone.now().date()

    def __str__(self):
        return f"{self.name} ({self.plan})"


class User(AbstractUser):
    """
    Custom User model linked to a Company.
    Supports different roles for SaaS access control.
    """
    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("staff", "Staff"),
        ("viewer", "Viewer"),
    )

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True, related_name="users"
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

    # Role helpers
    def is_owner(self):
        return self.role == "owner"

    def is_admin(self):
        return self.role == "admin"

    def is_manager(self):
        return self.role == "manager"

    def is_staff_user(self):
        return self.role == "staff"

    def is_viewer(self):
        return self.role == "viewer"


class Invite(models.Model):
    """
    Stores invitations for team members.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invites")
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES, default="viewer")
    token = models.CharField(max_length=100, unique=True)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite: {self.email} to {self.company.name}"
