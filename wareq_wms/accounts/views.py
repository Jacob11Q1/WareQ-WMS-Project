from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm

# Create your views here.

# Register
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:index')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# Login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:index')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


# Logout
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# Profile
def profile_view(request):
    return render(request, 'accounts/profile.html')