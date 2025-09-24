import factory
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating test users with roles.
    """

    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.LazyAttribute(lambda _: fake.unique.user_name())
    email = factory.LazyAttribute(lambda _: fake.unique.email())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())

    role = factory.LazyAttribute(lambda _: fake.random_element(["admin", "manager", "staff", "viewer"]))

    # Password will be hashed properly, but you can log in with "123456"
    password = factory.PostGenerationMethodCall("set_password", "123456")

    is_active = True
