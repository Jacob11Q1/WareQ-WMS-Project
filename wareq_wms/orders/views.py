from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db import transaction
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.utils.timezone import now, timedelta
from django.template.loader import render_to_string

# PDF generator (xhtml2pdf for better compatibility)
from xhtml2pdf import pisa
from io import BytesIO

from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet
from inventory.models import Item


# ============================================================
# DASHBOARD
# ============================================================
def index(request):
    """
    Orders dashboard.
    Shows quick stats and the 5 most recent orders.
    """
    orders = Order.objects.order_by("-created_at")
    context = {
        "sales_count": orders.filter(order_type="SALE").count(),
        "purchase_count": orders.filter(order_type="PURCHASE").count(),
        "pending_count": orders.filter(status="PENDING").count(),
        "completed_count": orders.filter(status="COMPLETED").count(),
        "recent_orders": orders[:5],
    }
    return render(request, "orders/index.html", context)


# ============================================================
# CRUD VIEWS
# ============================================================
def order_list(request):
    """
    Paginated list of all orders.
    Includes:
    - Filter by status
    - Search by customer or supplier
    """
    orders = (
        Order.objects
        .select_related("customer", "supplier")   # optimize queries
        .prefetch_related("items")                # preload items
        .order_by("-created_at")
    )

    # Filter by status (dropdown)
    status = request.GET.get("status", "")
    if status:
        orders = orders.filter(status=status)

    # Search by customer or supplier (query param)
    q = request.GET.get("q", "")
    if q:
        orders = orders.filter(
            Q(customer__name__icontains=q) |
            Q(supplier__name__icontains=q)
        )

    # Paginate results
    paginator = Paginator(orders, 10)  # 10 per page
    page = request.GET.get("page")
    orders = paginator.get_page(page)

    return render(request, "orders/order_list.html", {
        "orders": orders,
        "status": status,
        "q": q,
    })


def order_detail(request, pk):
    """
    Show details for a single order.
    Includes:
    - Customer/Supplier info
    - Items in the order
    - Status dropdown (AJAX powered)
    """
    order = get_object_or_404(
        Order.objects.prefetch_related("items__item"),
        pk=pk
    )
    return render(request, "orders/order_detail.html", {"order": order})


@transaction.atomic
def order_create(request):
    """
    Create a new order + order items (inline formset).
    Always starts with status = PENDING.
    """
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.status = "PENDING"   # enforce initial state
            order.save()

            # Link items to this order
            formset.instance = order
            formset.save()

            messages.success(request, f"Order #{order.id} created successfully!")
            return redirect("orders:order_detail", pk=order.id)
        else:
            messages.error(request, "Please fix the errors below.")

    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, "orders/order_form.html", {
        "form": form,
        "formset": formset,
    })


@transaction.atomic
def order_update(request, pk):
    """
    Edit an existing order.
    Business rules:
    - Completed/Cancelled orders cannot be edited.
    """
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

    return render(request, "orders/order_form.html", {
        "form": form,
        "formset": formset,
        "order": order,
    })


def order_delete(request, pk):
    """
    Delete confirmation page for an order.
    Business rules:
    - Completed orders cannot be deleted.
    """
    order = get_object_or_404(Order, pk=pk)

    if not order.can_be_deleted():
        messages.error(request, f"Order #{pk} cannot be deleted (already completed).")
        return redirect("orders:order_detail", pk=pk)

    if request.method == "POST":
        order.delete()
        messages.warning(request, f"Order #{pk} deleted.")
        return redirect("orders:order_list")

    return render(request, "orders/order_confirm_delete.html", {"order": order})


# ============================================================
# REPORTS & INVOICES
# ============================================================
def order_report(request):
    """
    Generate a report with:
    - Stats (sales, purchases, pending, etc.)
    - Monthly trend chart
    - Status pie chart
    - Recent 10 orders
    """
    orders = Order.objects.all()

    # Summary counts
    stats = {
        "total_orders": orders.count(),
        "sales_count": orders.filter(order_type="SALE").count(),
        "purchase_count": orders.filter(order_type="PURCHASE").count(),
        "pending_count": orders.filter(status="PENDING").count(),
        "completed_count": orders.filter(status="COMPLETED").count(),
        "cancelled_count": orders.filter(status="CANCELLED").count(),
    }

    # Last 5 months
    last_6_months = now().date().replace(day=1) - timedelta(days=150)
    monthly_orders = (
        orders.filter(created_at__gte=last_6_months)
        .extra(select={"month": "MONTH(created_at)"})
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    # By status
    status_data = (
        orders.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )

    context = {
        "stats": stats,
        "monthly_orders": list(monthly_orders),
        "status_data": list(status_data),
        "recent_orders": orders.order_by("-created_at")[:10],
    }
    return render(request, "orders/order_report.html", context)


def order_invoice(request, pk):
    """
    Generate invoice for a specific order.
    - Preview in browser (HTML)
    - Download as PDF (?format=pdf)
    """
    order = get_object_or_404(Order.objects.prefetch_related("items__item"), pk=pk)
    html = render_to_string("orders/order_invoice.html", {"order": order})

    # If PDF requested
    if request.GET.get("format") == "pdf":
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'filename="invoice_{order.id}.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)
        return response

    # Otherwise just render HTML
    return HttpResponse(html)


# ============================================================
# AJAX ENDPOINTS
# ============================================================
@require_POST
def update_status(request, pk):
    """
    AJAX endpoint to update order status without page reload.
    """
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get("status")

    try:
        order.status = new_status
        order.save()
        return JsonResponse({"success": True, "status": order.status})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def search_items(request):
    """
    AJAX endpoint for item autocomplete in order form.
    Returns top 10 matching items.
    """
    q = request.GET.get("q", "")
    items = Item.objects.filter(name__icontains=q)[:10]

    results = [
        {"id": item.id, "name": item.name, "price": str(item.price)}
        for item in items
    ]
    return JsonResponse(results, safe=False)
