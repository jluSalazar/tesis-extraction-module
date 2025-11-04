# design_app/factories.py
import factory
from factory.django import DjangoModelFactory

from projects.models import ResearchProject
from .models import ResearchQuestion # Asumiendo Project también está aquí

class ResearchQuestionFactory(DjangoModelFactory):
    class Meta:
        model = ResearchQuestion

    text = factory.Faker('paragraph', nb_sentences=1)
    project = factory.SubFactory(ResearchProject) # Si Project existe