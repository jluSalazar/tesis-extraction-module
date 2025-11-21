from .infrastructure.repositories.django_extraction_repository import DjangoExtractionRepository
from .infrastructure.repositories.django_tag_repository import DjangoTagRepository
from .domain.services.extraction_validator import ExtractionValidator
from .application.commands.create_extraction import CreateExtractionHandler
from .application.commands.complete_extraction import CompleteExtractionHandler


class Container:
    """
    Contenedor simple de inyección de dependencias.
    Se instancia en apps.py o se usa como Singleton/Module level.
    """

    # Repositories
    extraction_repository = DjangoExtractionRepository()
    tag_repository = DjangoTagRepository()  # Asumimos que existe

    # Domain Services
    extraction_validator = ExtractionValidator(tag_repository)

    # Command Handlers
    @property
    def create_extraction_handler(self):
        return CreateExtractionHandler(self.extraction_repository)

    @property
    def complete_extraction_handler(self):
        return CompleteExtractionHandler(
            self.extraction_repository,
            self.extraction_validator
        )


container = Container()