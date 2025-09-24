import factory
from faker import Faker
from .models import Customer

fake = Faker()


def safe_phone():
    """Generate a clean phone number (digits only, <= 15 chars)."""
    return fake.msisdn()[:15]


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.LazyAttribute(lambda _: fake.name())
    # Use sequence to guarantee uniqueness
    email = factory.Sequence(lambda n: f"customer{n}@{fake.free_email_domain()}")
    phone = factory.LazyFunction(safe_phone)
    address = factory.LazyAttribute(lambda _: fake.address())
    segment = factory.Iterator(["VIP", "REGULAR", "BLOCKED"])
    notes = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
    is_active = factory.LazyAttribute(lambda _: fake.boolean(chance_of_getting_true=90))
