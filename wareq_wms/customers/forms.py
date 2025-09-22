from django import forms
from django.core.exceptions import ValidationError
from .models import Customer


class CustomerForm(forms.ModelForm):
    """
    Form for adding and editing customers.
    """

    class Meta:
        model = Customer
        fields = ["name", "email", "phone", "address", "segment", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Address"}),
            "segment": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            phone = phone.strip()
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide is_active on create (only show on edit)
        if not self.instance or not self.instance.pk:
            self.fields.pop("is_active", None)
