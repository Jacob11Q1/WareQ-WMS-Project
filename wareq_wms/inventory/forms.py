from django import forms
from django.core.exceptions import ValidationError
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["sku", "name", "description", "quantity", "price", "supplier"]
        widgets = {
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter SKU"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter item name"}),
            "description": forms.Textarea(attrs={
                "class": "form-control", "rows": 3, "placeholder": "Optional description"
            }),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_sku(self):
        """Ensure SKU is unique."""
        sku = self.cleaned_data["sku"]
        if Item.objects.exclude(pk=self.instance.pk).filter(sku=sku).exists():
            raise ValidationError("This SKU already exists. Please choose another.")
        return sku

    def clean_quantity(self):
        """Prevent negative stock."""
        qty = self.cleaned_data["quantity"]
        if qty < 0:
            raise ValidationError("Quantity cannot be negative.")
        return qty


class StockAdjustmentForm(forms.Form):
    """Form to adjust stock for managers."""
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter adjustment (e.g., +10 or -5)"})
    )
    reason = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Reason for stock adjustment"}),
        max_length=255
    )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount == 0:
            raise ValidationError("Adjustment amount cannot be zero.")
        return amount
