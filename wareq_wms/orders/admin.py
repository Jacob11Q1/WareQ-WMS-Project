from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ("item", "quantity", "price", "total_price")
    readonly_fields = ("total_price",)

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = "Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order_type", "status", "customer", "supplier", "created_at", "updated_at")
    search_fields = ("customer__name", "supplier__name", "order_type", "status")
    list_filter = ("order_type", "status", "created_at")
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "item", "quantity", "price", "total_price")
    search_fields = ("order__id", "item__name")

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = "Total"