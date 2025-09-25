from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("dashboard/", views.index, name="index"),              # Orders dashboard
    path("", views.order_list, name="order_list"),              # List orders
    path("create/", views.order_create, name="order_create"),   # Create
    path("<int:pk>/", views.order_detail, name="order_detail"), # Detail
    path("<int:pk>/edit/", views.order_update, name="order_update"), # Update
    path("<int:pk>/delete/", views.order_delete, name="order_delete"), # Delete
    path("report/", views.order_report, name="order_report"),   # Reports
    path("<int:pk>/invoice/", views.order_invoice, name="order_invoice"), # Invoice

    # AJAX endpoints
    path("<int:pk>/update-status/", views.update_status, name="update_status"),
    path("search-items/", views.search_items, name="search_items"),
]
