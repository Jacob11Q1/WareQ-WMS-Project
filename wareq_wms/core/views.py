from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .form import ContactForm
from orders.models import Order
from customers.models import Customer
from suppliers.models import Supplier
from inventory.models import Item

def index(request):
    stats = {
        "items_count": Item.objects.count(),
        "orders_count": Order.objects.count(),
        "customers_count": Customer.objects.count(),
        "suppliers_count": Supplier.objects.count(),
    }
    return render(request, "core/index.html", {"stats": stats})

def about(request):
    return render(request, "core/about.html")

def dashboard(request):
    context = {
        "orders_count": Order.objects.count(),
        "customers_count": Customer.objects.count(),
        "suppliers_count": Supplier.objects.count(),
        "items_count": Item.objects.count(),
        "recent_orders": Order.objects.order_by("-id")[:5],
        "recent_customers": Customer.objects.order_by("-id")[:5],
    }
    return render(request, "core/dashboard.html", context)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you can send email or save to DB
            messages.success(request, "Your message has been sent! We'll get back to you soon.")
            return redirect("core:contact")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})
