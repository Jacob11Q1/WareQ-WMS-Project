from django.contrib import admin
from .models import Supplier, Item

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "is_active", "item_count", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("is_active", "created_at",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    actions = ["make_inactive", "make_active"]
    readonly_fields = ("created_at", "updated_at")

    @admin.action(description="Deactivate selected suppliers")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Reactivate selected suppliers")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sku", "supplier", "quantity", "price", "created_at")
    search_fields = ("name", "sku", "supplier__name")
    list_filter = ("supplier", "created_at")
    ordering = ("-created_at",)
