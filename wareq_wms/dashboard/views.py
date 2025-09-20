from django.shortcuts import render
from customers.models import Customer
from suppliers.models import Supplier
from inventory.models import Item
from orders.models import Order

def index(request):
    """
    Dashboard view showing system overview and recent activity.
    """
    stats = {
        "customers_count": Customer.objects.count(),
        "suppliers_count": Supplier.objects.count(),
        "items_count": Item.objects.count(),
        "orders_count": Order.objects.count(),
    }

    # Recent activity
    recent_orders = Order.objects.order_by("-created_at")[:5]
    recent_customers = Customer.objects.order_by("-created_at")[:5]
    recent_items = Item.objects.order_by("-created_at")[:5]

    return render(
        request,
        "dashboard/index.html",
        {
            "stats": stats,
            "recent_orders": recent_orders,
            "recent_customers": recent_customers,
            "recent_items": recent_items,
        },
    )
