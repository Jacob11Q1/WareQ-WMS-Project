from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
        "is_superuser",
        "date_joined",
        "created_at",
        "updated_at",
    )
    list_filter = ("role", "is_staff", "is_superuser", "created_at")
    search_fields = ("username", "email")
    readonly_fields = ("date_joined", "created_at", "updated_at")
    ordering = ("-date_joined",)
