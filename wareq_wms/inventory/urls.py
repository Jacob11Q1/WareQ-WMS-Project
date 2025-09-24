from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    # Dashboard
    path("dashboard/", views.index, name="index"),

    # CRUD
    path("", views.item_list, name="item_list"),
    path("create/", views.item_create, name="item_create"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    path("<int:pk>/edit/", views.item_update, name="item_update"),
    path("<int:pk>/delete/", views.item_delete, name="item_delete"),
    path("report/", views.stock_report, name="stock_report"),

    # AJAX / JSON endpoints
    path("search-items/", views.search_items, name="search_items"),
    path("validate-sku/", views.validate_sku, name="validate_sku"),
    path("<int:pk>/update-stock/", views.update_stock, name="update_stock"),
]
