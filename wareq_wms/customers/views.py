from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm
from django.utils import timezone


def index(request):
    """
    Dashboard view with stats + recent customers.
    """
    now = timezone.now()
    customers = Customer.objects.order_by("-created_at")

    context = {
        "total_customers": customers.count(),
        "recent_customers_count": customers.filter(
            created_at__year=now.year, created_at__month=now.month
        ).count(),
        "customers_with_email": customers.exclude(email="").count(),
        "recent_customers": customers[:5],
    }
    return render(request, "customers/index.html", context)


def customer_list(request):
    """
    List all customers with optional search.
    """
    search = request.GET.get("search", "")
    customers = Customer.objects.all()
    if search:
        customers = customers.filter(Q(name__icontains=search) | Q(email__icontains=search))

    return render(request, "customers/customer_list.html", {"customers": customers, "search": search})


def customer_detail(request, pk):
    """
    Show detailed profile of a single customer.
    """
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "customers/customer_detail.html", {"customer": customer})


def customer_create(request):
    """
    Create a new customer. Redirect → detail page.
    """
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, "Customer added successfully")
            return redirect("customers:customer_detail", pk=customer.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomerForm()
    return render(request, "customers/customer_form.html", {"form": form})


def customer_update(request, pk):
    """
    Edit an existing customer.
    """
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, "Customer updated successfully")
            return redirect("customers:customer_detail", pk=customer.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "customers/customer_form.html", {"form": form, "customer": customer})


def customer_delete(request, pk):
    """
    Delete a customer with confirmation page.
    """
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        messages.warning(request, f"Customer {customer.name} deleted")
        return redirect("customers:customer_list")
    return render(request, "customers/customer_confirm_delete.html", {"customer": customer})