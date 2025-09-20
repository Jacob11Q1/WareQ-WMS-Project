from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from orders.models import Order
from customers.models import Customer
from suppliers.models import Supplier
from inventory.models import Item
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    """
    Public homepage (landing page) with dynamic stats.
    """
    stats = {
        "items_count": Item.objects.count(),
        "orders_count": Order.objects.count(),
        "customers_count": Customer.objects.count(),
        "suppliers_count": Supplier.objects.count(),
    }

    return render(request, "core/index.html", {"stats": stats})


@login_required
def dashboard(request):
    """
    Private dashboard for logged-in users.
    Shows latest activity across modules.
    """
    recent_orders = Order.objects.order_by("-created_at")[:5]
    recent_customers = Customer.objects.order_by("-created_at")[:5]

    context = {
        "orders_count": Order.objects.count(),
        "customers_count": Customer.objects.count(),
        "suppliers_count": Supplier.objects.count(),
        "items_count": Item.objects.count(),
        "recent_orders": recent_orders,
        "recent_customers": recent_customers,
    }
    return render(request, "core/dashboard.html", context)


def about(request):
    """
    About page (static, but styled like SaaS).
    """
    return render(request, "core/about.html")


def contact(request):
    """
    Contact page with form to send messages.
    For now it just shows a success message (can later hook into email).
    """
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Example: print in console for now
        print(f"📩 New contact message from {name} ({email}): {message}")

        # If you want, enable Django email:
        # send_mail(
        #     subject=f"WareQ Contact from {name}",
        #     message=message,
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[settings.DEFAULT_FROM_EMAIL],
        # )

        success = True

    return render(request, "core/contact.html", {"success": success})