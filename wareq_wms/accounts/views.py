from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string

from .forms import RegisterForm, LoginForm, InviteForm
from .models import User, Company, Invite
from .decorators import owner_required, admin_or_owner_required


# -------------------------
# Authentication
# -------------------------

def register_view(request):
    """
    Registration now also creates a company.
    First registered user is the company Owner.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data["company_name"]

            # Create company
            company = Company.objects.create(
                name=company_name,
                plan="FREE",
                subscription_status="TRIAL",
            )

            # First user is Owner
            user = form.save(commit=False)
            user.company = company
            user.role = "owner"
            user.save()

            login(request, user)
            messages.success(request, f"Company {company_name} created! Account ready.")
            return redirect("core:dashboard")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """
    Log in existing users.
    """
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """
    Logout and redirect to login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


# -------------------------
# Profile
# -------------------------

@login_required
def profile_view(request):
    """
    Show current user's profile.
    """
    return render(request, "accounts/profile.html", {"user": request.user})


# -------------------------
# Company Settings
# -------------------------

@login_required
@owner_required
def company_settings(request):
    """
    Owners can update company information.
    """
    company = request.user.company
    if request.method == "POST":
        company.name = request.POST.get("name", company.name)
        company.save()
        messages.success(request, "Company updated successfully.")
        return redirect("accounts:company_settings")

    return render(request, "accounts/company_settings.html", {"company": company})


# -------------------------
# Team Invites
# -------------------------

@login_required
@admin_or_owner_required
def invite_user(request):
    """
    Owners/Admins can invite team members.
    """
    if request.method == "POST":
        form = InviteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            role = form.cleaned_data["role"]
            token = get_random_string(32)

            Invite.objects.create(
                company=request.user.company,
                email=email,
                role=role,
                token=token,
            )
            messages.success(request, f"Invite sent to {email}")
            return redirect("accounts:invite_user")
    else:
        form = InviteForm()

    invites = Invite.objects.filter(company=request.user.company, is_accepted=False)
    return render(request, "accounts/invite.html", {"form": form, "invites": invites})


# -------------------------
# User Management
# -------------------------

@login_required
@admin_or_owner_required
def user_list(request):
    """
    Show all users in the current company.
    """
    users = User.objects.filter(company=request.user.company).order_by("-date_joined")
    return render(request, "accounts/user_list.html", {"users": users})


@login_required
@admin_or_owner_required
def user_delete(request, pk):
    """
    Delete a user inside the same company.
    Owners cannot be deleted.
    """
    user = get_object_or_404(User, pk=pk, company=request.user.company)

    if request.method == "POST":
        if user.is_owner():
            messages.error(request, "You cannot delete the company owner.")
            return redirect("accounts:user_list")

        user.delete()
        messages.warning(request, f"User {user.username} deleted")
        return redirect("accounts:user_list")

    return render(request, "accounts/user_confirm_delete.html", {"user": user})


# -------------------------
# Billing (with dummy invoices)
# -------------------------

@login_required
@owner_required
def billing_dashboard(request):
    """
    Billing dashboard for company owner.
    Currently shows dummy invoices until Stripe/PayPal is integrated.
    """
    company = request.user.company

    invoices = [
        {"date": "2025-09-01", "amount": 49, "status": "paid", "url": "#"},
        {"date": "2025-08-01", "amount": 49, "status": "paid", "url": "#"},
        {"date": "2025-07-01", "amount": 49, "status": "unpaid", "url": "#"},
    ]

    return render(request, "accounts/billing.html", {
        "company": company,
        "invoices": invoices,
    })
