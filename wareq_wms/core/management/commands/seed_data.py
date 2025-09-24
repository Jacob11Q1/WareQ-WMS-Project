from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.utils import IntegrityError

from customers.factories import CustomerFactory
from suppliers.factories import SupplierFactory
from inventory.factories import ItemFactory, StockMovementFactory
from orders.factories import OrderFactory
from accounts.factories import UserFactory


def safe_create(factory_class, count, **kwargs):
    """
    Try to create objects with the factory, skip duplicates if IntegrityError is raised.
    Returns the list of created objects.
    """
    objs = []
    for _ in range(count):
        try:
            objs.append(factory_class.create(**kwargs))
        except IntegrityError:
            continue  # Skip duplicates and keep going
    return objs


class Command(BaseCommand):
    help = "Seed the database with dummy data (factories)."

    def add_arguments(self, parser):
        parser.add_argument("--customers", type=int, default=20)
        parser.add_argument("--suppliers", type=int, default=10)
        parser.add_argument("--items", type=int, default=50)
        parser.add_argument("--orders", type=int, default=100)
        parser.add_argument("--users", type=int, default=5)
        parser.add_argument("--flush", action="store_true", help="Flush DB before seeding")

    def handle(self, *args, **options):
        if options["flush"]:
            call_command("flush", "--noinput")
            self.stdout.write(self.style.WARNING("Database flushed!"))

        self.stdout.write(self.style.SUCCESS("Seeding database..."))

        # Customers & suppliers
        safe_create(CustomerFactory, options["customers"])
        safe_create(SupplierFactory, options["suppliers"])

        # Items
        items = safe_create(ItemFactory, options["items"])

        # Orders auto-create OrderItems
        safe_create(OrderFactory, options["orders"], items=items)

        # Users
        safe_create(UserFactory, options["users"])

        # Stock movements
        safe_create(StockMovementFactory, 30)

        self.stdout.write(self.style.SUCCESS("Dummy data generated successfully!"))
