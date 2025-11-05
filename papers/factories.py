import factory
from factory.django import DjangoModelFactory
from .models import Paper
from user_management.factories import UserFactory
# 1. Importar la nueva factory
from projects.factories import ProjectFactory


class PaperFactory(DjangoModelFactory):
    class Meta:
        model = Paper

    # 2. Añadir la FK obligatoria
    project = factory.SubFactory(ProjectFactory)

    title = factory.Faker('sentence', nb_words=10)
    authors = factory.Faker('name')
    year = factory.Faker('year')
    fulltext = factory.Faker('text', max_nb_chars=5000)
    #uploaded_by = factory.SubFactory(UserFactory)