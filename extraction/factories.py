import factory
from factory.django import DjangoModelFactory

# Importas factories de OTRAS apps
from papers.factories import PaperFactory
from user_management.factories import UserFactory
from design.factories import ResearchQuestionFactory  # Necesario para Tags

# Importas modelos de TU app (usando el __init__.py)
from .models import Quote, ExtractionRecord, Tag, Comment


class ExtractionRecordFactory(DjangoModelFactory):
    class Meta:
        # 1. Corregir el modelo
        model = ExtractionRecord

    paper = factory.SubFactory(PaperFactory)
    status = 'Pending'
    assigned_to = factory.SubFactory(UserFactory)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.Faker('word')
    color = factory.Faker('hex_color')
    created_by = factory.SubFactory(UserFactory)
    question = factory.SubFactory(ResearchQuestionFactory)  # Asociar a una pregunta
    is_mandatory = factory.Faker('boolean', chance_of_getting_true=25)


class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote

    text_portion = factory.Faker('paragraph')
    # 2. Corregir la FK: Quote se enlaza a ExtractionRecord, no a Paper
    paper = factory.SubFactory(ExtractionRecordFactory)
    researcher = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:  # Permite pasar una lista de tags al crear
            for tag in extracted:
                self.tags.add(tag)
        else:
            # Añade 2 tags aleatorios si no se pasan
            self.tags.add(TagFactory(), TagFactory())


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    quote = factory.SubFactory(QuoteFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Faker('sentence')
    is_review = factory.Faker('boolean', chance_of_getting_true=50)