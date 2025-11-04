import factory
from factory.django import DjangoModelFactory
from .models import CustomUser # O el nombre de tu modelo

class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ('username',) # Evita duplicados

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    is_staff = False