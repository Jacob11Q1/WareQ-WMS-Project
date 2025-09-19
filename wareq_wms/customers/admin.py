from django.contrib import admin
from .models import Customer

# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")