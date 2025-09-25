from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Company


class RegisterForm(UserCreationForm):
    """
    Extended registration form:
    - If the user is the owner, they create a company.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"})
    )
    company_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Company name"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "company_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Choose a username"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Re-enter password"}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username/email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )


class InviteForm(forms.Form):
    """
    Form for company admins/owners to invite team members.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
