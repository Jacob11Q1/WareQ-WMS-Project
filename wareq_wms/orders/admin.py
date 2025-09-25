from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline display of items inside an order (admin panel)."""
    model = OrderItem
    extra = 1
    fields = ("item", "quantity", "price", "total_price")
    readonly_fields = ("total_price",)

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = "Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin management for Orders."""
    list_display = ("id", "order_type", "status", "customer", "supplier", "created_at")
    list_display_links = ("id", "order_type")
    search_fields = ("customer__name", "supplier__name", "status")
    list_filter = ("order_type", "status", "created_at")
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin management for line items."""
    list_display = ("order", "item", "quantity", "price", "total_price")

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = "Total"
