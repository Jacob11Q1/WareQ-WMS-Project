from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q, Sum, F
from datetime import timedelta

from .models import Supplier, Item
from .forms import SupplierForm, ItemForm


# ---------------------------
# Dashboard
# ---------------------------
def index(request):
    suppliers = Supplier.objects.all()
    items = Item.objects.all()
    now = timezone.now()

    recent_suppliers = suppliers.filter(
        created_at__year=now.year, created_at__month=now.month
    ).order_by("-created_at")[:5]

    context = {
        "suppliers": suppliers,
        "total_suppliers": suppliers.count(),
        "active_suppliers": suppliers.filter(is_active=True).count(),
        "inactive_suppliers": suppliers.filter(is_active=False).count(),
        "total_items": items.count(),
        "total_catalog_value": items.aggregate(
            total=Sum(F("quantity") * F("price"))
        )["total"] or 0,
        "recent_suppliers": recent_suppliers,
    }
    return render(request, "suppliers/index.html", context)


# ---------------------------
# Supplier CRUD
# ---------------------------
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by("-created_at")
    context = {
        "suppliers": suppliers,
        "total_suppliers": suppliers.count(),
        "active_suppliers": suppliers.filter(is_active=True).count(),
    }
    return render(request, "suppliers/supplier_list.html", context)


def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    items = supplier.supplier_items.all()
    context = {
        "supplier": supplier,
        "items": items,
        "catalog_value": supplier.catalog_value,
        "item_count": supplier.item_count,
        "latest_item": supplier.latest_item,
        "average_price": supplier.average_price,
    }
    return render(request, "suppliers/supplier_detail.html", context)


def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f"Supplier '{supplier.name}' created.")
            return redirect(reverse("suppliers:supplier_detail", args=[supplier.id]))
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SupplierForm()
    return render(request, "suppliers/supplier_form.html", {"form": form})


def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, f"Supplier '{supplier.name}' updated.")
            return redirect(reverse("suppliers:supplier_detail", args=[pk]))
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SupplierForm(instance=supplier)
    return render(request, "suppliers/supplier_form.html", {"form": form, "supplier": supplier})


def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.deactivate()
        messages.warning(request, f"Supplier '{supplier.name}' deactivated.")
        return redirect(reverse("suppliers:supplier_list"))
    return render(request, "suppliers/supplier_confirm_delete.html", {"supplier": supplier})


def supplier_reactivate(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.reactivate()
        messages.success(request, f"Supplier '{supplier.name}' reactivated.")
        return redirect(reverse("suppliers:supplier_detail", args=[pk]))
    return redirect(reverse("suppliers:supplier_detail", args=[pk]))


# ---------------------------
# Item Management
# ---------------------------
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Item '{item.name}' added for {item.supplier.name}.")
            return redirect(reverse("suppliers:supplier_detail", args=[item.supplier.id]))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ItemForm()
    return render(request, "suppliers/item_form.html", {"form": form})


# ---------------------------
# JSON / AJAX Endpoints
# ---------------------------
def api_list(request):
    search = request.GET.get("search", "")
    active = request.GET.get("active", "")
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 10))

    qs = Supplier.objects.all().order_by("-created_at")
    if active == "1":
        qs = qs.filter(is_active=True)
    elif active == "0":
        qs = qs.filter(is_active=False)

    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)

    data = {
        "results": [
            {
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "phone": s.phone or "-",
                "address": s.address or "-",
                "created": s.created_at.strftime("%b %d, %Y"),
                "is_active": s.is_active,
                "item_count": s.item_count,
                "catalog_value": float(s.catalog_value),
                "detail_url": reverse("suppliers:supplier_detail", args=[s.id]),
                "edit_url": reverse("suppliers:supplier_update", args=[s.id]),
                "delete_url": reverse("suppliers:supplier_delete", args=[s.id]),
            }
            for s in page_obj
        ],
        "page": page_obj.number,
        "num_pages": page_obj.paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_prev": page_obj.has_previous(),
    }
    return JsonResponse(data)


def api_search(request):
    q = request.GET.get("q", "")
    qs = Supplier.objects.filter(is_active=True)
    if q:
        qs = qs.filter(
            Q(name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q)
        )
    qs = qs[:10]
    return JsonResponse(
        [{"id": s.id, "name": s.name, "email": s.email} for s in qs],
        safe=False
    )


def api_stats(request):
    now = timezone.now()
    start = (now - timedelta(days=180)).replace(day=1)
    monthly = {}
    qs = Supplier.objects.filter(created_at__gte=start, is_active=True)

    for s in qs:
        key = s.created_at.strftime("%Y-%m")
        monthly[key] = monthly.get(key, 0) + 1

    labels, values = [], []
    for i in range(5, -1, -1):
        d = (now.replace(day=1) - timedelta(days=30 * i))
        key = d.strftime("%Y-%m")
        labels.append(d.strftime("%b %Y"))
        values.append(monthly.get(key, 0))

    data = {
        "total": Supplier.objects.filter(is_active=True).count(),
        "new_this_month": Supplier.objects.filter(
            is_active=True, created_at__year=now.year, created_at__month=now.month
        ).count(),
        "labels": labels,
        "values": values,
        "items_total": Item.objects.count(),
        "active_ratio": {
            "active": Supplier.objects.filter(is_active=True).count(),
            "inactive": Supplier.objects.filter(is_active=False).count(),
        }
    }
    return JsonResponse(data)


def validate_email(request):
    email = (request.GET.get("email") or "").strip().lower()
    exclude = request.GET.get("exclude")
    qs = Supplier.objects.filter(email=email)
    if exclude and exclude.isdigit():
        qs = qs.exclude(pk=int(exclude))
    return JsonResponse({"exists": qs.exists()})


def validate_sku(request):
    sku = (request.GET.get("sku") or "").strip()
    exclude = request.GET.get("exclude")
    qs = Item.objects.filter(sku=sku)
    if exclude and exclude.isdigit():
        qs = qs.exclude(pk=int(exclude))
    return JsonResponse({"exists": qs.exists()})
