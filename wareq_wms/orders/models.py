from django.db import models, transaction
from django.core.exceptions import ValidationError
from customers.models import Customer
from suppliers.models import Supplier
from inventory.models import Item


class Order(models.Model):
    ORDER_TYPES = (
        ("SALE", "Sale"),
        ("PURCHASE", "Purchase"),
    )

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} - {self.order_type} ({self.status})"

    # -------------------------------
    # PHASE 4 ADDITIONS
    # -------------------------------

    def can_be_deleted(self):
        """Only allow delete if not completed."""
        return self.status not in ["COMPLETED"]

    def is_editable(self):
        """Lock editing for completed/cancelled orders."""
        return self.status in ["PENDING", "PROCESSING"]

    @transaction.atomic
    def apply_stock_changes(self):
        """
        Apply stock changes when order is completed.
        SALE → reduce stock.
        PURCHASE → increase stock.
        """
        for item in self.items.all():
            if self.order_type == "SALE":
                if item.item.quantity < item.quantity:
                    raise ValidationError(
                        f"Not enough stock for {item.item.name}. "
                        f"Available: {item.item.quantity}, Required: {item.quantity}"
                    )
                item.item.quantity -= item.quantity
            elif self.order_type == "PURCHASE":
                item.item.quantity += item.quantity
            item.item.save()

    def save(self, *args, **kwargs):
        """
        Override save to enforce business rules:
        - Prevent rollback from COMPLETED/CANCELLED.
        - Apply stock changes when status = COMPLETED.
        """
        if self.pk:
            old = Order.objects.get(pk=self.pk)
            # Prevent rollback of completed/cancelled
            if old.status in ["COMPLETED", "CANCELLED"] and old.status != self.status:
                raise ValidationError(f"Cannot change status from {old.status} back to {self.status}")

            # When moving to COMPLETED → update stock
            if old.status != "COMPLETED" and self.status == "COMPLETED":
                self.apply_stock_changes()

        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

    def save(self, *args, **kwargs):
        if not self.price:  # auto-fill from inventory
            self.price = self.item.price
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} * {self.item.name} (Order {self.order.id})"
