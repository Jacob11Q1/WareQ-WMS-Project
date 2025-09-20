from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)  # avoid duplicates
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # track creation
    updated_at = models.DateTimeField(auto_now=True)      # track updates

    def __str__(self):
        return self.name


# 🔹 Connect Supplier to its Items (separate from inventory)
class Item(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="supplier_items"
    )
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.supplier.name})"