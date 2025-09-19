from django.db import models

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)  # prevent duplicates
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp for consistency
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name