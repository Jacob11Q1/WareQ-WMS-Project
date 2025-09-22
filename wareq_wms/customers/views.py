from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm
from datetime import timedelta


@login_required
def index(request):
    """
    Dashboard view with stats + recent customers.
    """
    now = timezone.now()
    customers = Customer.objects.order_by("-created_at")

    context = {
        "total_customers": customers.filter(is_active=True).count(),
        "recent_customers_count": customers.filter(
            created_at__year=now.year, created_at__month=now.month, is_active=True
        ).count(),
        "customers_with_email": customers.filter(is_active=True).exclude(email="").count(),
        "recent_customers": customers.filter(is_active=True)[:5],
    }
    return render(request, "customers/index.html", context)


@login_required
def customer_list(request):
    """
    List all customers with optional search & filters & pagination.
    """
    search = request.GET.get("search", "")
    active = request.GET.get("active", "1")  # default show only active
    has_email = request.GET.get("has_email", "")

    qs = Customer.objects.all()
    if active == "1":
        qs = qs.filter(is_active=True)
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search))
    if has_email == "1":
        qs = qs.exclude(email="")

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "customers/customer_list.html", {
        "customers": page_obj,
        "search": search,
        "active": active,
        "has_email": has_email,
    })


@login_required
def customer_detail(request, pk):
    """
    Show detailed profile of a single customer.
    """
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "customers/customer_detail.html", {"customer": customer})


@login_required
def customer_create(request):
    """
    Create a new customer. Redirect → detail page.
    """
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, "Customer added successfully")
            return redirect("customers:customer_detail", pk=customer.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomerForm()
    return render(request, "customers/customer_form.html", {"form": form})


@login_required
def customer_update(request, pk):
    """
    Edit an existing customer.
    """
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, "Customer updated successfully")
            return redirect("customers:customer_detail", pk=customer.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "customers/customer_form.html", {"form": form, "customer": customer})


@login_required
def customer_delete(request, pk):
    """
    Soft-delete (deactivate) a customer with confirmation page.
    """
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.deactivate()
        messages.warning(request, f"Customer {customer.name} deactivated")
        return redirect("customers:customer_list")
    return render(request, "customers/customer_confirm_delete.html", {"customer": customer})


@login_required
@require_POST
def customer_reactivate(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.reactivate()
    messages.success(request, f"Customer {customer.name} reactivated")
    return redirect("customers:customer_detail", pk=pk)


# ---------------------------
# JSON / AJAX Endpoints
# ---------------------------

@login_required
def api_list(request):
    """
    JSON list for customers table (AJAX) with filters & pagination.
    """
    search = request.GET.get("search", "")
    active = request.GET.get("active", "1")
    has_email = request.GET.get("has_email", "")

    qs = Customer.objects.all()
    if active == "1":
        qs = qs.filter(is_active=True)
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search))
    if has_email == "1":
        qs = qs.exclude(email="")

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    data = {
        "results": [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone or "-",
                "created": c.created_at.strftime("%b %d, %Y"),
                "segment": c.segment,
                "is_active": c.is_active,
                "detail_url": f"/customers/{c.id}/",
                "edit_url": f"/customers/{c.id}/edit/",
                "delete_url": f"/customers/{c.id}/delete/",
            }
            for c in page_obj
        ],
        "page": page_obj.number,
        "num_pages": page_obj.paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_prev": page_obj.has_previous(),
    }
    return JsonResponse(data)


@login_required
def api_search(request):
    """
    Typeahead search (top 10).
    """
    q = request.GET.get("q", "")
    qs = Customer.objects.filter(is_active=True)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q))
    qs = qs[:10]
    return JsonResponse([{"id": c.id, "name": c.name, "email": c.email} for c in qs], safe=False)


@login_required
def api_stats(request):
    """
    Stats for dashboard widgets & small chart (last 6 months).
    """
    now = timezone.now()
    start = (now - timedelta(days=180)).replace(day=1)
    monthly = {}
    qs = Customer.objects.filter(created_at__gte=start, is_active=True)

    # group in Python (DB-agnostic)
    for c in qs:
        key = c.created_at.strftime("%Y-%m")
        monthly[key] = monthly.get(key, 0) + 1

    labels = []
    values = []
    # 6 months including current month
    for i in range(5, -1, -1):
        d = (now.replace(day=1) - timedelta(days=30 * i))
        key = d.strftime("%Y-%m")
        labels.append(d.strftime("%b %Y"))
        values.append(monthly.get(key, 0))

    data = {
        "total": Customer.objects.filter(is_active=True).count(),
        "with_email": Customer.objects.filter(is_active=True).exclude(email="").count(),
        "new_this_month": Customer.objects.filter(
            is_active=True, created_at__year=now.year, created_at__month=now.month
        ).count(),
        "labels": labels,
        "values": values,
    }
    return JsonResponse(data)


@login_required
def validate_email(request):
    """
    Live unique email validation.
    Accepts optional ?exclude=<id> to ignore current record on edit.
    """
    email = request.GET.get("email", "")
    exclude = request.GET.get("exclude")
    qs = Customer.objects.filter(email=email)
    if exclude and exclude.isdigit():
        qs = qs.exclude(pk=int(exclude))
    return JsonResponse({"exists": qs.exists()})
