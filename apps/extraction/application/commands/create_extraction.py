from dataclasses import dataclass
from django.db import transaction
from ...domain.repositories.i_extraction_repository import IExtractionRepository
from ...domain.entities.extraction import Extraction
from ...domain.value_objects.extraction_status import ExtractionStatus
from ...domain.exceptions.extraction_exceptions import StudyNotFound

@dataclass
class CreateExtractionCommand:
    study_id: int
    user_id: int


class CreateExtractionHandler:
    def __init__(self, repository: IExtractionRepository, study_adapter):
        self.repository = repository
        self.study_adapter = study_adapter

    @transaction.atomic
    def handle(self, command: CreateExtractionCommand) -> Extraction:
        existing = self.repository.get_by_study_id(command.study_id)
        if existing:
            return existing
        if not self.study_adapter.exists(command.study_id):
            raise StudyNotFound(  # ✅ Excepción específica
                f"El estudio {command.study_id} no existe"
            )

        new_extraction = Extraction(
            id=None,
            study_id=command.study_id,
            assigned_to_user_id=command.user_id,
            status=ExtractionStatus.PENDING
        )

        saved_extraction = self.repository.save(new_extraction)
        return saved_extraction