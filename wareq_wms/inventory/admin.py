from django.contrib import admin
from .models import Item, StockMovement


class StockMovementInline(admin.TabularInline):
    model = StockMovement
    extra = 0
    readonly_fields = ("change", "old_quantity", "new_quantity", "reason", "updated_by", "created_at")
    can_delete = False
    ordering = ("-created_at",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "quantity", "price", "supplier", "created_at", "updated_at")
    list_editable = ("quantity", "price")  # quick inline editing
    search_fields = ("name", "sku", "description", "supplier__name")
    list_filter = ("supplier", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")

    inlines = [StockMovementInline]


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("item", "change", "old_quantity", "new_quantity", "reason", "updated_by", "created_at")
    list_filter = ("created_at", "updated_by")
    search_fields = ("item__sku", "item__name", "reason")
    readonly_fields = ("item", "change", "old_quantity", "new_quantity", "reason", "updated_by", "created_at")
    ordering = ("-created_at",)
