from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    """Form for creating/updating an Order."""

    class Meta:
        model = Order
        fields = ["order_type", "customer", "supplier", "status"]
        widgets = {
            "order_type": forms.Select(attrs={"class": "form-select custom-select"}),
            "customer": forms.Select(attrs={"class": "form-select custom-select"}),
            "supplier": forms.Select(attrs={"class": "form-select custom-select"}),
            "status": forms.Select(attrs={"class": "form-select custom-select"}),
        }


class OrderItemForm(forms.ModelForm):
    """Form for managing individual line items."""

    class Meta:
        model = OrderItem
        fields = ["item", "quantity", "price"]
        widgets = {
            "item": forms.Select(attrs={"class": "form-select custom-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control custom-input", "min": "1"}),
            "price": forms.NumberInput(attrs={"class": "form-control custom-input", "step": "0.01"}),
        }


# Inline formset: allows multiple OrderItems inside one Order
OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True
)
