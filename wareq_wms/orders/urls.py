from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # Dashboard / index
    path("dashboard/", views.index, name="index"),

    # CRUD operations
    path("", views.order_list, name="order_list"),
    path("create/", views.order_create, name="order_create"),
    path("<int:pk>/", views.order_detail, name="order_detail"),
    path("<int:pk>/edit/", views.order_update, name="order_update"),
    path("<int:pk>/delete/", views.order_delete, name="order_delete"),
    
    # Reports
    path("report/", views.order_report, name="order_report"),

    # AJAX endpoints
    path("<int:pk>/update-status/", views.update_status, name="update_status"),
    path("search-items/", views.search_items, name="search_items"),
]
