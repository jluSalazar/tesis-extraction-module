import factory
from factory.django import DjangoModelFactory
from django.contrib.contenttypes.models import ContentType

# --- 1. Importaciones de MODELOS de otras apps (NO factories) ---
from papers.models import Paper
from projects.models import ResearchProject
from design.models import ResearchQuestion
from user_management.models import CustomUser

# --- 2. Importaciones de tus modelos LOCALES ---
from .models import Quote, PaperExtraction, Tag, Comment


# -----------------------------------------------------------------
# --- 3. FAKE FACTORIES (Contrato de prueba local) ---
#    Estas son simulaciones de las factories externas.
#    Las nombramos con '_' para indicar que son internas.
# -----------------------------------------------------------------

class _FakeUserFactory(DjangoModelFactory):
    """Simulación local de user_management.factories.UserFactory"""

    class Meta:
        model = CustomUser
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    is_staff = False


class _FakeProjectFactory(DjangoModelFactory):
    """Simulación local de projects.factories.ProjectFactory"""

    class Meta:
        model = ResearchProject
        django_get_or_create = ('title',)

    title = factory.Faker('catch_phrase')
    description = factory.Faker('paragraph')
    owner = factory.SubFactory(_FakeUserFactory)
    status = ResearchProject.Status.EXTRACTION_ACTIVE


class _FakeResearchQuestionFactory(DjangoModelFactory):
    """Simulación local de design.factories.ResearchQuestionFactory"""

    class Meta:
        model = ResearchQuestion

    text = factory.Faker('paragraph', nb_sentences=1)
    project = factory.SubFactory(_FakeProjectFactory)
    # Asumimos que el modelo ResearchQuestion tiene más campos,
    # pero solo necesitamos los mínimos para que el 'create' funcione.


class _FakePaperFactory(DjangoModelFactory):
    """
    Simulación local de papers.factories.PaperFactory
    Esta es la respuesta a tu pregunta.
    """

    class Meta:
        model = Paper

    # 1. Usamos nuestra _FakeProjectFactory
    project = factory.SubFactory(_FakeProjectFactory)

    # 2. Llenamos los campos que Paper necesita
    title = factory.Faker('sentence', nb_words=10)
    authors = factory.Faker('name')
    year = factory.Faker('year')
    fulltext = factory.Faker('text', max_nb_chars=1000)
    # No necesitamos 'uploaded_by' si es 'null=True'


# -----------------------------------------------------------------
# --- 4. FACTORIES REALES de 'extraction' (Actualizadas) ---
#    Estas son las factories de tu app, que ahora usan
#    las 'Fakes' locales, no las importaciones externas.
# -----------------------------------------------------------------

class PaperExtractionFactory(DjangoModelFactory):
    """
    Factory para tu modelo 'PaperExtraction'.
    (Nombre actualizado desde ExtractionRecordFactory para coincidir con el modelo).
    """

    class Meta:
        model = PaperExtraction  # 👈 Modelo correcto

    # ✅ RESPUESTA: Usa la _FakePaperFactory local
    paper = factory.SubFactory(_FakePaperFactory)

    status = PaperExtraction.Status.PENDING

    # ✅ Usa la _FakeUserFactory local
    assigned_to = factory.SubFactory(_FakeUserFactory)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.Faker('word')
    color = factory.Faker('hex_color')

    # ✅ Usa la _FakeUserFactory local
    created_by = factory.SubFactory(_FakeUserFactory)

    # ✅ Usa la _FakeResearchQuestionFactory local
    question = factory.SubFactory(_FakeResearchQuestionFactory)

    is_mandatory = factory.Faker('boolean', chance_of_getting_true=25)


class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote

    text_portion = factory.Faker('paragraph')

    # ✅ Actualizado: El campo se llama 'paper_extraction' y usa la factory local
    paper_extraction = factory.SubFactory(PaperExtractionFactory)

    # ✅ Usa la _FakeUserFactory local
    researcher = factory.SubFactory(_FakeUserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            # Usa la TagFactory local
            self.tags.add(TagFactory(), TagFactory())


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    # ✅ Usa la _FakeUserFactory local
    user = factory.SubFactory(_FakeUserFactory)
    text = factory.Faker('sentence')
    is_review = factory.Faker('boolean', chance_of_getting_true=50)

    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(Quote)
    )
    object_id = factory.SelfAttribute('content_object.id')

    # ✅ Usa la QuoteFactory local
    content_object = factory.SubFactory(QuoteFactory)


class TagCommentFactory(CommentFactory):
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(Tag)
    )
    # ✅ Usa la TagFactory local
    content_object = factory.SubFactory(TagFactory)