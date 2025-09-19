from django.contrib import admin
from .models import Supplier

# Register your models here.

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"