import factory
from faker import Faker
from django.utils import timezone
from decimal import Decimal
from .models import Order, OrderItem
from customers.factories import CustomerFactory
from suppliers.factories import SupplierFactory
from inventory.factories import ItemFactory

fake = Faker()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    order_type = factory.LazyAttribute(lambda _: fake.random_element(["SALE", "PURCHASE"]))
    status = factory.LazyAttribute(lambda _: fake.random_element(
        ["PENDING", "PROCESSING", "COMPLETED", "CANCELLED"]
    ))

    # Link customer only if SALE, supplier only if PURCHASE
    customer = factory.Maybe(
        factory.LazyAttribute(lambda o: o.order_type == "SALE"),
        yes_declaration=factory.SubFactory(CustomerFactory),
        no_declaration=None,
    )
    supplier = factory.Maybe(
        factory.LazyAttribute(lambda o: o.order_type == "PURCHASE"),
        yes_declaration=factory.SubFactory(SupplierFactory),
        no_declaration=None,
    )

    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        """Auto-create OrderItems after Order is created"""
        if not create:
            return

        if extracted:  # If we pass items manually
            for item in extracted:
                OrderItemFactory(order=self, item=item)
        else:  # Otherwise generate random items
            for _ in range(fake.random_int(min=1, max=3)):
                OrderItemFactory(order=self)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory, items=None)  # prevent recursion
    item = factory.SubFactory(ItemFactory)
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=10))
    price = factory.SelfAttribute("item.price")  # always matches item price
