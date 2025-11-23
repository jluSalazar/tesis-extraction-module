from .infrastructure.adapters.acquisition_service_adapter import AcquisitionServiceAdapter
from .infrastructure.adapters.design_service_adapter import DesignServiceAdapter
from .infrastructure.repositories.django_extraction_repository import DjangoExtractionRepository
from .infrastructure.repositories.django_tag_repository import DjangoTagRepository
from .domain.services.extraction_validator import ExtractionValidator
from .application.commands.create_extraction import CreateExtractionHandler
from .application.commands.complete_extraction import CompleteExtractionHandler
from .infrastructure.repositories.django_quote_repository import DjangoQuoteRepository
from .domain.services.tag_merger import TagMergeService
from .application.commands.create_quote import CreateQuoteHandler
from .application.commands.create_tag import CreateTagHandler
from .application.commands.moderate_tag import ModerateTagHandler
from .application.commands.merge_tags import MergeTagsHandler


class Container:
    # Repositories
    extraction_repository = DjangoExtractionRepository()
    quote_repository = DjangoQuoteRepository()
    study_adapter = AcquisitionServiceAdapter()
    tag_repository = DjangoTagRepository(study_adapter)
    design_repository = DesignServiceAdapter()

    # Domain Services
    extraction_validator = ExtractionValidator(tag_repository)
    tag_merger = TagMergeService(quote_repository, tag_repository)

    # Command Handlers
    @property
    def create_extraction_handler(self):
        return CreateExtractionHandler(self.extraction_repository, self.study_adapter)

    @property
    def complete_extraction_handler(self):
        return CompleteExtractionHandler(self.extraction_repository, self.extraction_validator)

    @property
    def create_quote_handler(self):  # Nuevo
        return CreateQuoteHandler(
            extraction_repo=self.extraction_repository,
            quote_repo=self.quote_repository,
            tag_repo=self.tag_repository
        )

    @property
    def create_tag_handler(self):  # Nuevo
        return CreateTagHandler(
            tag_repo=self.tag_repository,
            design_repo=self.design_repository  # Inyectamos el adaptador de Design
        )

    @property
    def moderate_tag_handler(self):  # Nuevo
        return ModerateTagHandler(self.tag_repository)

    @property
    def merge_tags_handler(self):  # Nuevo
        return MergeTagsHandler(self.tag_repository, self.quote_repository, self.tag_merger)


container = Container()