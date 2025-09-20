from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "quantity", "price", "supplier", "created_at")
    list_editable = ("quantity", "price")  # quick inline editing
    search_fields = ("name", "sku", "description")
    list_filter = ("created_at", "supplier")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
