from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Custom admin interface for managing customers.
    """
    list_display = ("id", "name", "email", "phone", "segment", "is_active", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("segment", "is_active", "created_at")
    readonly_fields = ("created_at", "updated_at")
    actions = ["make_inactive", "make_active"]

    @admin.action(description="Deactivate selected customers")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Reactivate selected customers")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
