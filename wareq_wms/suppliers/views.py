from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Supplier, Item
from .forms import SupplierForm, ItemForm

# Dashboard
def index(request):
    suppliers = Supplier.objects.all()
    items = Item.objects.all()
    context = {
        "suppliers": suppliers,
        "total_suppliers": suppliers.count(),
        "total_items": items.count(),
    }
    return render(request, "suppliers/index.html", context)


# List all suppliers
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by("-created_at")
    return render(request, "suppliers/supplier_list.html", {"suppliers": suppliers})


# Supplier detail (with their items)
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    items = supplier.items.all()
    return render(request, "suppliers/supplier_detail.html", {"supplier": supplier, "items": items})


# Create supplier
def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f"Supplier '{supplier.name}' created.")
            return redirect(reverse("suppliers:supplier_list"))
    else:
        form = SupplierForm()
    return render(request, "suppliers/supplier_form.html", {"form": form})


# Update supplier
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, f"Supplier '{supplier.name}' updated.")
            return redirect(reverse("suppliers:supplier_list"))
    else:
        form = SupplierForm(instance=supplier)
    return render(request, "suppliers/supplier_form.html", {"form": form})


# Delete supplier
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
        messages.success(request, f"Supplier '{supplier.name}' deleted.")
        return redirect(reverse("suppliers:supplier_list"))
    return render(request, "suppliers/supplier_confirm_delete.html", {"supplier": supplier})


# Manage items under suppliers
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Item '{item.name}' added for {item.supplier.name}.")
            return redirect(reverse("suppliers:supplier_detail", args=[item.supplier.id]))
    else:
        form = ItemForm()
    return render(request, "suppliers/item_form.html", {"form": form})
