from dataclasses import dataclass
from typing import List
from django.db import transaction
from ...domain.entities.quote import Quote
from ...domain.repositories.i_extraction_repository import IExtractionRepository
from ...domain.repositories.i_quote_repository import IQuoteRepository
from ...domain.repositories.i_tag_repository import ITagRepository
from ...domain.repositories.i_acquisition_repository import IAcquisitionRepository
from ...domain.exceptions.extraction_exceptions import (
    ExtractionNotFound,
    UnauthorizedExtractionAccess,
    InvalidExtractionState,
    TagNotFound,
    ExtractionValidationError
)


@dataclass
class CreateQuoteCommand:
    extraction_id: int
    text: str
    location: str
    user_id: int
    tag_ids: List[int]


class CreateQuoteHandler:
    def __init__(
            self,
            extraction_repo: IExtractionRepository,
            quote_repo: IQuoteRepository,
            tag_repo: ITagRepository,
            acquisition_adapter: IAcquisitionRepository
    ):
        self.extraction_repo = extraction_repo
        self.quote_repo = quote_repo
        self.tag_repo = tag_repo
        self.acquisition_adapter = acquisition_adapter

    @transaction.atomic
    def handle(self, command: CreateQuoteCommand) -> Quote:
        extraction = self.extraction_repo.get_by_id(command.extraction_id)
        if not extraction:
            raise ExtractionNotFound(
                f"Extracción {command.extraction_id} no encontrada"
            )

        if extraction.assigned_to_user_id != command.user_id:
            raise UnauthorizedExtractionAccess(
                "No tienes permiso para agregar quotes a esta extracción"
            )

        tags = self.tag_repo.get_by_ids(command.tag_ids)
        if len(tags) != len(command.tag_ids):
            found_ids = {t.id for t in tags}
            missing = set(command.tag_ids) - found_ids
            raise TagNotFound(f"Tags no encontrados: {missing}")

        project_id = self.acquisition_adapter.get_project_context(
            extraction.study_id
        )
        if not project_id:
            raise ExtractionValidationError(
                "No se pudo determinar el proyecto de la extracción"
            )

        for tag in tags:
            if tag.project_id != project_id:
                raise ExtractionValidationError(
                    f"El tag '{tag.name}' no pertenece al proyecto actual"
                )

        from ...domain.value_objects.tag_status import TagStatus
        for tag in tags:
            if tag.status != TagStatus.APPROVED:
                # Solo permitir tags pending si son del mismo usuario (inductivos)
                if tag.created_by_user_id != command.user_id:
                    raise ExtractionValidationError(
                        f"El tag '{tag.name}' no está aprobado para uso"
                    )

        quote = Quote(
            id=None,
            extraction_id=command.extraction_id,
            text=command.text,
            location=command.location,
            researcher_id=command.user_id,
            tags=tags
        )

        extraction.add_quote(quote)

        return self.quote_repo.save(quote)