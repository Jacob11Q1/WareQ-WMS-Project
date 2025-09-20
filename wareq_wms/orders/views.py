from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Order
from .forms import OrderForm, OrderItemFormSet


def index(request):
    """Orders dashboard with stats + recent orders."""
    orders = Order.objects.order_by("-created_at")
    context = {
        "sales_count": orders.filter(order_type="SALE").count(),
        "purchase_count": orders.filter(order_type="PURCHASE").count(),
        "pending_count": orders.filter(status="PENDING").count(),
        "completed_count": orders.filter(status="COMPLETED").count(),
        "recent_orders": orders[:5],  # show last 5 orders
    }
    return render(request, "orders/index.html", context)


def order_list(request):
    """List all orders with filters and totals."""
    orders = Order.objects.select_related("customer", "supplier").prefetch_related("items").order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})


def order_detail(request, pk):
    """Detailed view of one order with its items."""
    order = get_object_or_404(Order.objects.prefetch_related("items__item"), pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})


@transaction.atomic
def order_create(request):
    """Create a new order with inline items (formset)."""
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.instance = order
            formset.save()
            messages.success(request, f"✅ Order #{order.id} created successfully!")
            return redirect("orders:order_detail", pk=order.id)
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, "orders/order_form.html", {"form": form, "formset": formset})


@transaction.atomic
def order_update(request, pk):
    """Update order and its items."""
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"✅ Order #{order.id} updated successfully!")
            return redirect("orders:order_detail", pk=order.id)
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    return render(request, "orders/order_form.html", {"form": form, "formset": formset, "order": order})


def order_delete(request, pk):
    """Confirm and delete an order."""
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        messages.warning(request, f"🗑️ Order #{pk} deleted.")
        return redirect("orders:order_list")
    return render(request, "orders/order_confirm_delete.html", {"order": order})
