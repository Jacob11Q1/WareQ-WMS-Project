from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["sku", "name", "description", "quantity", "price", "supplier"]

        widgets = {
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter SKU"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter item name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional description"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
        }
