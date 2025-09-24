from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required

from .models import Item, StockMovement
from .forms import ItemForm, StockAdjustmentForm
from django.db.models import Sum, Count


# ----------------------------
# Dashboard
# ----------------------------
@login_required
def index(request):
    items = Item.objects.all()
    low_stock = items.filter(quantity__lte=5).count()
    out_of_stock = items.filter(quantity=0).count()

    movements = StockMovement.objects.select_related("item").order_by("-created_at")[:5]

    context = {
        "items": items,
        "total_items": items.count(),
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "recent_movements": movements,
    }
    return render(request, "inventory/index.html", context)


# ----------------------------
# Item List
# ----------------------------
@login_required
def item_list(request):
    query = request.GET.get("q")
    items = Item.objects.all()

    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(sku__icontains=query) | Q(supplier__name__icontains=query)
        )

    paginator = Paginator(items, 10)  # 10 per page
    page = request.GET.get("page")
    items_page = paginator.get_page(page)

    return render(request, "inventory/item_list.html", {"items": items_page, "query": query})


# ----------------------------
# Item Detail
# ----------------------------
@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    movements = item.movements.all()[:10]  # last 10 movements
    adjustment_form = StockAdjustmentForm()

    if request.method == "POST":
        adjustment_form = StockAdjustmentForm(request.POST)
        if adjustment_form.is_valid():
            amount = adjustment_form.cleaned_data["amount"]
            reason = adjustment_form.cleaned_data["reason"]
            try:
                item.adjust_stock(amount, reason, user=request.user)
                messages.success(request, f"Stock updated for {item.name}.")
                return redirect("inventory:item_detail", pk=item.id)
            except Exception as e:
                messages.error(request, str(e))

    return render(request, "inventory/item_detail.html", {
        "item": item,
        "movements": movements,
        "adjustment_form": adjustment_form,
    })


# ----------------------------
# Create / Update / Delete
# ----------------------------
@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully.")
            return redirect("inventory:item_list")
    else:
        form = ItemForm()
    return render(request, "inventory/item_form.html", {"form": form})


@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item {item.name} updated successfully.")
            return redirect("inventory:item_detail", pk=item.id)
    else:
        form = ItemForm(instance=item)
    return render(request, "inventory/item_form.html", {"form": form, "item": item})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        if item.quantity > 0:
            messages.error(request, f"Cannot delete {item.name}. Stock is not empty.")
            return redirect("inventory:item_detail", pk=item.id)
        item.delete()
        messages.warning(request, f"Item {item.name} deleted.")
        return redirect("inventory:item_list")
    return render(request, "inventory/item_confirm_delete.html", {"item": item})

def stock_report(request):
    """Report page for inventory stock levels."""
    items = Item.objects.all()

    stats = {
        "total_items": items.count(),
        "low_stock": items.filter(quantity__lte=5).count(),
        "out_of_stock": items.filter(quantity=0).count(),
        "total_quantity": items.aggregate(total=Sum("quantity"))["total"] or 0,
    }

    return render(request, "inventory/stock_report.html", {
        "stats": stats,
        "items": items.order_by("name"),
    })


# ----------------------------
# AJAX Endpoints
# ----------------------------
@login_required
def search_items(request):
    """Return JSON list of items for autocomplete search."""
    q = request.GET.get("q", "")
    items = Item.objects.filter(Q(name__icontains=q) | Q(sku__icontains=q))[:10]
    data = [{"id": i.id, "sku": i.sku, "name": i.name, "quantity": i.quantity, "price": str(i.price)} for i in items]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
@permission_required("inventory.change_item", raise_exception=True)
def update_stock(request, pk):
    """Adjust stock via AJAX."""
    item = get_object_or_404(Item, pk=pk)
    amount = int(request.POST.get("amount", 0))
    reason = request.POST.get("reason", "Manual update")
    try:
        item.adjust_stock(amount, reason, user=request.user)
        return JsonResponse({"success": True, "new_quantity": item.quantity})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def validate_sku(request):
    """Live check if SKU exists."""
    sku = request.GET.get("sku", "")
    exists = Item.objects.filter(sku=sku).exists()
    return JsonResponse({"exists": exists})
