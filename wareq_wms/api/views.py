from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission
from django_filters.rest_framework import DjangoFilterBackend

from customers.models import Customer
from suppliers.models import Supplier, Item
from orders.models import Order
from .serializers import CustomerSerializer, SupplierSerializer, ItemSerializer, OrderSerializer


# Custom permission: only admins can delete
class IsAdminOrReadUpdate(BasePermission):
    """
    Allow read and update for authenticated users,
    but only admin users can delete objects.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method in ["POST", "PUT", "PATCH"]:
            return request.user.is_authenticated
        if request.method == "DELETE":
            return request.user.is_staff or request.user.is_superuser
        return False


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Customers.
    Supports search, ordering, and filtering.
    """
    queryset = Customer.objects.all().order_by("-created_at")
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadUpdate]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["name", "email", "phone"]
    ordering_fields = ["created_at", "name"]
    filterset_fields = ["is_active"]  # Example field
    ordering = ["-created_at"]


class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Suppliers.
    """
    queryset = Supplier.objects.all().order_by("-created_at")
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadUpdate]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["name", "email", "phone"]
    ordering_fields = ["created_at", "name"]
    filterset_fields = ["is_active"]
    ordering = ["-created_at"]


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Inventory Items.
    """
    queryset = Item.objects.all().order_by("-created_at")
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadUpdate]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["name", "sku", "description"]
    ordering_fields = ["price", "quantity", "created_at"]
    filterset_fields = ["supplier", "is_active"]
    ordering = ["-created_at"]


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Orders.
    """
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadUpdate]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["customer__name", "supplier__name", "status", "order_type"]
    ordering_fields = ["created_at", "status", "order_type"]
    filterset_fields = ["status", "order_type", "customer", "supplier"]
    ordering = ["-created_at"]
