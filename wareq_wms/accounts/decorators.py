from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps


def owner_required(view_func):
    """
    Restrict access to company owners only.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_owner():
            messages.error(request, "Only company owners can access this page.")
            return redirect("core:dashboard")
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_or_owner_required(view_func):
    """
    Restrict access to company owners or admins.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not (
            request.user.is_owner() or request.user.is_admin()
        ):
            messages.error(request, "You don’t have permission to access this page.")
            return redirect("core:dashboard")
        return view_func(request, *args, **kwargs)
    return wrapper
