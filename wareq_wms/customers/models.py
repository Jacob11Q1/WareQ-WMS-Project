from django.db import models

phone = models.CharField(
    max_length=30,   # or 50 if you want to be extra safe
    blank=True,
    null=True,
    db_index=True
)

class Customer(models.Model):
    """
    Customer model representing clients in the system.
    Includes audit timestamps (created_at, updated_at).
    """

    SEGMENT_CHOICES = (
        ("VIP", "VIP"),
        ("REGULAR", "Regular"),
        ("BLOCKED", "Blocked"),
    )

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, db_index=True)  # enforce unique email
    phone = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    address = models.TextField(blank=True, null=True)

    # 🔽 Phase 4 additions
    segment = models.CharField(max_length=20, choices=SEGMENT_CHOICES, default="REGULAR")
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, help_text="When this customer was first added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last time this customer record was updated.")

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def reactivate(self):
        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
