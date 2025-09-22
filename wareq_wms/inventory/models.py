from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.conf import settings
from suppliers.models import Supplier


class Item(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0, help_text="Current stock level")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per unit")
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventory_items"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------------
    # Phase 4 Additions
    # -------------------------------

    def is_low_stock(self):
        """Check if stock is low."""
        return self.quantity <= 5

    @transaction.atomic
    def adjust_stock(self, amount: int, reason: str, user=None):
        """
        Safely adjust stock and log movement.
        :param amount: positive for increase, negative for decrease
        :param reason: string describing why
        :param user: user performing action (optional)
        """
        old_qty = self.quantity
        new_qty = old_qty + amount

        if new_qty < 0:
            raise ValidationError(f"Cannot reduce stock below 0 for {self.name} (SKU {self.sku}).")

        self.quantity = new_qty
        self.save()

        # Create stock movement log
        StockMovement.objects.create(
            item=self,
            change=amount,
            old_quantity=old_qty,
            new_quantity=new_qty,
            reason=reason,
            updated_by=user if user else None,
        )

    def __str__(self):
        return f"{self.name} ({self.sku})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Item"
        verbose_name_plural = "Items"


class StockMovement(models.Model):
    """Log every stock adjustment for audit/history."""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="movements")
    change = models.IntegerField()  # +10 for add, -5 for remove
    old_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        sign = "+" if self.change > 0 else ""
        return f"{self.item.sku} {sign}{self.change} (New: {self.new_quantity})"
