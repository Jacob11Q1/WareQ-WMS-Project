import factory
from faker import Faker
from decimal import Decimal
from .models import Item, StockMovement
from suppliers.factories import SupplierFactory

fake = Faker()


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    sku = factory.LazyAttribute(lambda _: fake.unique.bothify(text="INV-####"))
    name = factory.LazyAttribute(lambda _: fake.word().capitalize() + " " + fake.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=8))
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=200))
    price = factory.LazyAttribute(
        lambda _: Decimal(str(fake.pydecimal(left_digits=4, right_digits=2, positive=True)))
    )
    supplier = factory.SubFactory(SupplierFactory)


class StockMovementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockMovement

    item = factory.SubFactory(ItemFactory)
    change = factory.LazyAttribute(lambda _: fake.random_int(-20, 50))

    @factory.lazy_attribute
    def old_quantity(self):
        return max(0, fake.random_int(min=0, max=50))

    @factory.lazy_attribute
    def new_quantity(self):
        return max(0, self.old_quantity + self.change)

    reason = factory.LazyAttribute(lambda _: fake.sentence(nb_words=6))
    updated_by = None  # later link with UserFactory
