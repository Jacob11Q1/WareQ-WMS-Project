from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path("", views.customer_list, name="customer_list"),  # main page
    path("dashboard/", views.index, name="index"),        # optional summary/dashboard
    path("create/", views.customer_create, name="customer_create"),
    path("<int:pk>/edit/", views.customer_update, name="customer_update"),
    path("<int:pk>/delete/", views.customer_delete, name="customer_delete"),
]