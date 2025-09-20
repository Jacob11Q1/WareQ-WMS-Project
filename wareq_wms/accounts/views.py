from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User


# Register
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("core:index")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# Login
def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f" Welcome back, {user.username}!")
            # Role-based redirect
            if user.is_admin():
                return redirect("accounts:user_list")
            return redirect("core:index")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


# Logout
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


# Profile
@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})


# Admin-only: list all users
@login_required
@user_passes_test(lambda u: u.is_admin())
def user_list(request):
    users = User.objects.all().order_by("-date_joined")
    return render(request, "accounts/user_list.html", {"users": users})


# Admin-only: delete a user
@login_required
@user_passes_test(lambda u: u.is_admin())
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.warning(request, f"User {user.username} deleted")
        return redirect("accounts:user_list")
    return render(request, "accounts/user_confirm_delete.html", {"user": user})
