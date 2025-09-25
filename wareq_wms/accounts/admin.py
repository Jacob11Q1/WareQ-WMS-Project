from django.contrib import admin
from .models import User, Company, Invite


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "company",
        "is_staff",
        "is_superuser",
        "date_joined",
        "created_at",
        "updated_at",
    )
    list_filter = ("role", "is_staff", "is_superuser", "company", "created_at")
    search_fields = ("username", "email")
    readonly_fields = ("date_joined", "created_at", "updated_at")
    ordering = ("-date_joined",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "plan", "subscription_status", "trial_end", "created_at")
    list_filter = ("plan", "subscription_status")
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ("email", "company", "role", "is_accepted", "created_at")
    list_filter = ("role", "is_accepted")
    search_fields = ("email", "company__name")
    ordering = ("-created_at",)
