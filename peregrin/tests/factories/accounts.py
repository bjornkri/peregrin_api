import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    email = factory.Faker('email')

    class Meta:
        model = User
