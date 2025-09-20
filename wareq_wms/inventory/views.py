from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm

def index(request):
    items = Item.objects.all()
    low_stock = items.filter(quantity__lte=5).count()
    context = {
        "items": items,
        "total_items": items.count(),
        "low_stock": low_stock,
    }
    return render(request, "inventory/index.html", context)

def item_list(request):
    items = Item.objects.all()
    return render(request, "inventory/item_list.html", {"items": items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "inventory/item_detail.html", {"item": item})

def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list")
    else:
        form = ItemForm()
    return render(request, "inventory/item_form.html", {"form": form})

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list")
    else:
        form = ItemForm(instance=item)
    return render(request, "inventory/item_form.html", {"form": form})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect("inventory:item_list")
    return render(request, "inventory/item_confirm_delete.html", {"item": item})
