from django.db import models
from suppliers.models import Supplier

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0, help_text="Current stock level")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per unit")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name="items")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    class Meta:
        ordering = ['-created_at']  # Show newest items first
        verbose_name = "Item"
        verbose_name_plural = "Items"