from django.contrib import admin
from .models import Item

# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'quantity', 'price', 'created_at', 'updated_at')
    list_editable = ('quantity', 'price')  # Quick inline editing
    search_fields = ('name', 'sku', 'description')  # If you add description field
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)  # Newest items first
    date_hierarchy = 'created_at'  # Date-based drill-down navigation