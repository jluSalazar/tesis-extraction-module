# extraction_app/factories.py
import factory
from factory.django import DjangoModelFactory

# ¡Importas las factories de las OTRAS apps!
from papers.factories import PaperFactory
from design.factories import ResearchQuestionFactory

# Importas tus propios modelos (usando el nuevo paquete)
from .models import Quote, Tag

class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.Faker('word')
    color = factory.Faker('hex_color')
    type = 'inductive'
    question = factory.SubFactory(ResearchQuestionFactory) # Crea la dependencia

class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote

    text_portion = factory.Faker('paragraph', nb_sentences=4)
    location = factory.Faker('random_int', min=1, max=100, step=1)

    # Aquí está la magia:
    # factory-boy crea un Paper usando PaperFactory automáticamente
    paper = factory.SubFactory(PaperFactory)

    # Añade un tag aleatorio (si la relación M2M existe)
    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            # Crea un tag por defecto si no se pasó ninguno
            self.tags.add(TagFactory())