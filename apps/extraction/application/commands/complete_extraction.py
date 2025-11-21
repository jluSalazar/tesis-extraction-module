from dataclasses import dataclass
from ...domain.repositories.i_extraction_repository import IExtractionRepository
from ...domain.services.extraction_validator import ExtractionValidator
from ...domain.exceptions.extraction_exceptions import ExtractionValidationError


@dataclass
class CompleteExtractionCommand:
    extraction_id: int
    user_id: int


class CompleteExtractionHandler:
    def __init__(self,
                 repository: IExtractionRepository,
                 validator: ExtractionValidator):
        self.repository = repository
        self.validator = validator

    def handle(self, command: CompleteExtractionCommand):
        # 1. Obtener Agregado
        extraction = self.repository.get_by_id(command.extraction_id)
        if not extraction:
            raise ExtractionValidationError("Extracción no encontrada")

        # 2. Validar seguridad (básico)
        if extraction.assigned_to_user_id != command.user_id:
            raise ExtractionValidationError("No tienes permiso para completar esta extracción")

        # 3. Lógica de Dominio (Validador y Entidad)
        missing_tags = self.validator.validate_completeness(extraction)

        # 4. Mutar estado de la entidad
        extraction.complete(missing_mandatory_tags=missing_tags)

        # 5. Persistir
        self.repository.save(extraction)