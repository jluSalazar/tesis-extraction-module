import factory
from factory.django import DjangoModelFactory
from django.contrib.contenttypes.models import ContentType

from papers.factories import PaperFactory
from user_management.factories import UserFactory
from design.factories import ResearchQuestionFactory
from .models import Quote, ExtractionRecord, Tag, Comment


class ExtractionRecordFactory(DjangoModelFactory):
    class Meta:
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
    question = factory.SubFactory(ResearchQuestionFactory)
    is_mandatory = factory.Faker('boolean', chance_of_getting_true=25)


class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote

    text_portion = factory.Faker('paragraph')
    paper = factory.SubFactory(ExtractionRecordFactory)
    researcher = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(TagFactory(), TagFactory())


class CommentFactory(DjangoModelFactory):
    """
    Factory para Comments usando GenericForeignKey.
    Por defecto crea comentarios para Quotes.
    """

    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    text = factory.Faker('sentence')
    is_review = factory.Faker('boolean', chance_of_getting_true=50)

    # GenericForeignKey fields
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(Quote)
    )
    object_id = factory.SelfAttribute('content_object.id')
    content_object = factory.SubFactory(QuoteFactory)


# Factory alternativa para comentarios en Tags
class TagCommentFactory(CommentFactory):
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(Tag)
    )
    content_object = factory.SubFactory(TagFactory)