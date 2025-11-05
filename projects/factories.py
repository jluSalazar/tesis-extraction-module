import factory
from factory.django import DjangoModelFactory
from .models import ResearchProject
from user_management.factories import UserFactory

class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = ResearchProject
        django_get_or_create = ('title',) # Evitar duplicados

    title = factory.Faker('catch_phrase')
    description = factory.Faker('paragraph', nb_sentences=3)
    owner = factory.SubFactory(UserFactory)
    status = ResearchProject.Status.EXTRACTION_ACTIVE