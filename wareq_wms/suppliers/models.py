from django.db import models
from django.core.validators import MinValueValidator


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, db_index=True)  # avoid duplicates
    phone = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    address = models.TextField(blank=True, null=True)

    # Phase 4 – Active status (soft delete)
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)  # track creation
    updated_at = models.DateTimeField(auto_now=True)      # track updates

    # Soft delete & reactivation
    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=["is_active", "updated_at"])

    def reactivate(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=["is_active", "updated_at"])

    # Extra computed fields
    @property
    def item_count(self):
        """Total items linked to this supplier."""
        return self.supplier_items.count()

    @property
    def catalog_value(self):
        """Total value of all stock from this supplier."""
        return sum(i.quantity * i.price for i in self.supplier_items.all())

    @property
    def latest_item(self):
        """Most recently added item (quick access for dashboards)."""
        return self.supplier_items.order_by("-created_at").first()

    @property
    def average_price(self):
        """Average unit price across this supplier's items."""
        qs = self.supplier_items.all()
        return round(sum(i.price for i in qs) / qs.count(), 2) if qs.exists() else 0

    def __str__(self):
        status = "✅" if self.is_active else "❌"
        return f"{self.name} {status}"


# 🔹 Connect Supplier to its Items (separate from inventory)
class Item(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="supplier_items"
    )
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Stock level (must be >= 0)"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price per unit"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Convenience fields
    @property
    def total_value(self):
        """Total value of this stock item (qty * price)."""
        return self.quantity * self.price

    def __str__(self):
        return f"{self.name} ({self.supplier.name})"
