import factory
from factory.django import DjangoModelFactory
from .models import Paper
from user_management.factories import UserFactory # Dependencia

class PaperFactory(DjangoModelFactory):
    class Meta:
        model = Paper

    title = factory.Faker('sentence', nb_words=10)
    authors = factory.Faker('name')
    year = factory.Faker('year')
    fulltext = factory.Faker('text', max_nb_chars=5000)
    # Asumiendo que 'uploaded_by' existe, aunque no lo listaste
    uploaded_by = factory.SubFactory(UserFactory)