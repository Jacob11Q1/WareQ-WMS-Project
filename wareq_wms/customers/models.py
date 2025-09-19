from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, help_text="When this customer was first added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last time this customer record was updated.")

    def __str__(self):
        return f"{self.name} ({self.email})"