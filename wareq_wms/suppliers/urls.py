from django.urls import path
from . import views

app_name = "suppliers"

urlpatterns = [
    # Dashboard & List
    path("", views.supplier_list, name="supplier_list"),
    path("dashboard/", views.index, name="index"),

    # Supplier CRUD
    path("create/", views.supplier_create, name="supplier_create"),
    path("<int:pk>/", views.supplier_detail, name="supplier_detail"),
    path("<int:pk>/edit/", views.supplier_update, name="supplier_update"),
    path("<int:pk>/delete/", views.supplier_delete, name="supplier_delete"),
    path("<int:pk>/reactivate/", views.supplier_reactivate, name="supplier_reactivate"),  # 🔹 restore deleted

    # Item management (under supplier)
    path("items/create/", views.item_create, name="item_create"),

    # JSON / AJAX APIs
    path("api/list/", views.api_list, name="api_list"),       # 🔹 list suppliers JSON
    path("api/search/", views.api_search, name="api_search"), # 🔹 search suppliers
    path("api/stats/", views.api_stats, name="api_stats"),    # 🔹 dashboard stats
    path("validate/email/", views.validate_email, name="validate_email"),  # 🔹 live email check
    path("validate/sku/", views.validate_sku, name="validate_sku"),        # 🔹 live SKU check
]
