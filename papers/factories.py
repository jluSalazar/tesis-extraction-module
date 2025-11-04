# papers_app/factories.py
import factory
from factory.django import DjangoModelFactory
from .models import Paper # Importa su propio modelo

class PaperFactory(DjangoModelFactory):
    class Meta:
        model = Paper
        # Evita crear duplicados si el título es el mismo
        django_get_or_create = ('title',)

    title = factory.Faker('sentence', nb_words=8)
    authors = factory.Faker('name')
    year = factory.Faker('year')
    fulltext = factory.Faker('text', max_nb_chars=5000)
    status = 'Pending'
    # 'uploaded_by' (User) se puede añadir con SubFactory si es necesario
    # uploaded_by = factory.SubFactory(UserFactory)