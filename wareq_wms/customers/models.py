from django.db import models


class Customer(models.Model):
    """
    Customer model representing clients in the system.
    Includes audit timestamps (created_at, updated_at).
    """

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, db_index=True)  # enforce unique email
    phone = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    address = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, help_text="When this customer was first added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last time this customer record was updated.")

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
