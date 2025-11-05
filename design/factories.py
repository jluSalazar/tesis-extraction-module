import factory
from factory.django import DjangoModelFactory

# 1. Importar la nueva factory
from projects.factories import ProjectFactory 
from .models import ResearchQuestion

class ResearchQuestionFactory(DjangoModelFactory):
    class Meta:
        model = ResearchQuestion

    text = factory.Faker('paragraph', nb_sentences=1)
    # 2. Corregir la SubFactory
    project = factory.SubFactory(ProjectFactory)