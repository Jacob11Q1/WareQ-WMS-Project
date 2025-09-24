import factory
from faker import Faker
from .models import Supplier, Item

fake = Faker()


def safe_phone():
    """Generate a clean phone number (digits only, <= 15 chars)."""
    return fake.msisdn()[:15]


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.LazyAttribute(lambda _: fake.company())
    # Guarantee uniqueness with sequence
    email = factory.Sequence(lambda n: f"supplier{n}@{fake.free_email_domain()}")
    phone = factory.LazyFunction(safe_phone)
    address = factory.LazyAttribute(lambda _: fake.address())
    is_active = factory.LazyAttribute(lambda _: fake.boolean(chance_of_getting_true=90))


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    supplier = factory.SubFactory(SupplierFactory)
    name = factory.LazyAttribute(lambda _: f"{fake.word().capitalize()} {fake.word().capitalize()}")
    # Ensure SKU uniqueness with sequence
    sku = factory.Sequence(lambda n: f"SKU-{n:05d}")
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=500))
    price = factory.LazyAttribute(
        lambda _: round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2)
    )
