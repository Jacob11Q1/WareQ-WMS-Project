from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.item_list, name="item_list"),  # main page
    path("dashboard/", views.index, name="index"),  # optional dashboard/summary
    path("create/", views.item_create, name="item_create"),
    path("<int:pk>/edit/", views.item_update, name="item_update"),
    path("<int:pk>/delete/", views.item_delete, name="item_delete"),
]
