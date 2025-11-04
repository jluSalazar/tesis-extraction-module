import factory
from factory.django import DjangoModelFactory

# Importas factories de OTRAS apps
from papers.factories import PaperFactory
from user_management.factories import UserFactory

# Importas modelos de TU app (asumiendo que los refactorizaste)
from .models.core import Quote
from .models.records import ExtractionPaper
from .models.tagging import Tag

class ExtractionRecordFactory(DjangoModelFactory):
    class Meta:
        model = ExtractionPaper

    paper = factory.SubFactory(PaperFactory) # ¡Crea un Paper automáticamente!
    status = 'Pending'
    assigned_to = factory.SubFactory(UserFactory)

class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.Faker('word')
    color = factory.Faker('hex_color')
    # ...

class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote

    # Para que esta factory funcione, necesita un ExtractionRecord
    # PERO Quote tiene FK a Paper, no a ExtractionRecord...
    # Corrijamos tu modelo original: Quote DEBERÍA tener FK a ExtractionRecord
    # Si Quote.paper es FK(Paper):
    text_portion = factory.Faker('paragraph')
    paper = factory.SubFactory(PaperFactory) # Asumiendo FK a Paper
    researcher = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if create:
            self.tags.add(TagFactory()) # Añade un tag