from django.shortcuts import render
from customers.models import Customer
from suppliers.models import Supplier
from inventory.models import Item
from orders.models import Order

# Create your views here.

def index(request):
    stats = {
        "customers": Customer.objects.count(),
        "suppliers": Supplier.objects.count(),
        "items": Item.objects.count(),
        "orders": Order.objects.count(),
    }

    recent_orders = Order.objects.order_by("-created_at")[:5]
    recent_items = Item.objects.order_by("-created_at")[:5]

    return render(request, "dashboard/index.html", {
        "stats": stats,
        "recent_orders": recent_orders,
        "recent_items": recent_items,
    })