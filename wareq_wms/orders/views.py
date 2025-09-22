from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet
from inventory.models import Item


def index(request):
    """Orders dashboard with stats + recent orders."""
    orders = Order.objects.order_by("-created_at")
    context = {
        "sales_count": orders.filter(order_type="SALE").count(),
        "purchase_count": orders.filter(order_type="PURCHASE").count(),
        "pending_count": orders.filter(status="PENDING").count(),
        "completed_count": orders.filter(status="COMPLETED").count(),
        "recent_orders": orders[:5],
    }
    return render(request, "orders/index.html", context)


def order_list(request):
    """List all orders with filters, search, and pagination."""
    orders = Order.objects.select_related("customer", "supplier").prefetch_related("items").order_by("-created_at")

    # Filter by status
    status = request.GET.get("status")
    if status:
        orders = orders.filter(status=status)

    # Search by customer/supplier
    q = request.GET.get("q")
    if q:
        orders = orders.filter(
            Q(customer__name__icontains=q) |
            Q(supplier__name__icontains=q)
        )

    # Pagination
    paginator = Paginator(orders, 10)  # 10 orders per page
    page = request.GET.get("page")
    orders = paginator.get_page(page)

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
            order = form.save(commit=False)
            order.status = "PENDING"  # always start pending
            order.save()
            formset.instance = order
            formset.save()
            messages.success(request, f"Order #{order.id} created successfully!")
            return redirect("orders:order_detail", pk=order.id)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, "orders/order_form.html", {"form": form, "formset": formset})


@transaction.atomic
def order_update(request, pk):
    """Update order and its items."""
    order = get_object_or_404(Order, pk=pk)

    if not order.is_editable():
        messages.warning(request, "Completed/Cancelled orders cannot be edited.")
        return redirect("orders:order_detail", pk=order.id)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"Order #{order.id} updated successfully!")
            return redirect("orders:order_detail", pk=order.id)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    return render(request, "orders/order_form.html", {"form": form, "formset": formset, "order": order})


def order_delete(request, pk):
    """Confirm and delete an order."""
    order = get_object_or_404(Order, pk=pk)

    if not order.can_be_deleted():
        messages.error(request, f"Order #{pk} cannot be deleted (already completed).")
        return redirect("orders:order_detail", pk=pk)

    if request.method == "POST":
        order.delete()
        messages.warning(request, f"Order #{pk} deleted.")
        return redirect("orders:order_list")

    return render(request, "orders/order_confirm_delete.html", {"order": order})


# -------------------------
# AJAX Endpoints
# -------------------------

@require_POST
def update_status(request, pk):
    """AJAX: update order status without page reload."""
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get("status")

    try:
        order.status = new_status
        order.save()
        return JsonResponse({"success": True, "status": order.status})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def search_items(request):
    """AJAX: search items for autocomplete in order form."""
    q = request.GET.get("q", "")
    items = Item.objects.filter(name__icontains=q)[:10]  # limit results
    results = [{"id": item.id, "name": item.name, "price": str(item.price)} for item in items]
    return JsonResponse(results, safe=False)
