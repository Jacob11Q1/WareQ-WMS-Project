from django import forms
from .models import Supplier, Item

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "email", "phone", "address"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Supplier Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Address"}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["supplier", "name", "sku", "description", "quantity", "price"]

        widgets = {
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Item Name"}),
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "Unique SKU"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Item Description"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }
