from django.contrib import admin
from .models import Supplier, Item

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sku", "supplier", "quantity", "price", "created_at")
    search_fields = ("name", "sku", "supplier__name")
    list_filter = ("supplier", "created_at")
    ordering = ("-created_at",)
