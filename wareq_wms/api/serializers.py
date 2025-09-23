from rest_framework import serializers
from customers.models import Customer
from suppliers.models import Supplier, Item
from orders.models import Order


# ----------------------
# Expandable Base
# ----------------------
class ExpandableSerializerMixin(serializers.ModelSerializer):
    """
    Allows ?expand=field1,field2 to include nested serializers.
    Example: /api/v1/orders/1/?expand=customer,supplier
    """

    def __init__(self, *args, **kwargs):
        expand = None
        request = self.context.get("request")
        if request:
            expand = request.query_params.get("expand", "")
            expand = [f.strip() for f in expand.split(",") if f.strip()]

        super().__init__(*args, **kwargs)

        if expand:
            for field in expand:
                if hasattr(self, "expandable_fields") and field in self.expandable_fields:
                    self.fields[field] = self.expandable_fields[field](context=self.context)

    class Meta:
        abstract = True


# ----------------------
# Customer
# ----------------------
class CustomerSerializer(ExpandableSerializerMixin):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone", "address", "created_at"]
        read_only_fields = ["id", "created_at"]

    expandable_fields = {}


# ----------------------
# Supplier
# ----------------------
class SupplierSerializer(ExpandableSerializerMixin):
    item_count = serializers.IntegerField(source="supplier_items.count", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address",
            "is_active",
            "item_count",
            "created_at",
        ]
        read_only_fields = ["id", "item_count", "created_at"]

    expandable_fields = {
        "items": lambda **kwargs: ItemSerializer(many=True, read_only=True, **kwargs),
    }


# ----------------------
# Item
# ----------------------
class ItemSerializer(ExpandableSerializerMixin):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "sku",
            "description",
            "price",
            "quantity",
            "supplier",
            "supplier_name",
            "created_at",
        ]
        read_only_fields = ["id", "supplier_name", "created_at"]

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    expandable_fields = {
        "supplier": lambda **kwargs: SupplierSerializer(read_only=True, **kwargs),
    }


# ----------------------
# Order
# ----------------------
class OrderSerializer(ExpandableSerializerMixin):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_type",
            "status",
            "customer",
            "supplier",
            "total_amount",
            "created_at",
        ]
        read_only_fields = ["id", "total_amount", "created_at"]

    expandable_fields = {
        "customer": lambda **kwargs: CustomerSerializer(read_only=True, **kwargs),
        "supplier": lambda **kwargs: SupplierSerializer(read_only=True, **kwargs),
    }
