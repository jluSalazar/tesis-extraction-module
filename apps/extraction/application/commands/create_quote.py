from dataclasses import dataclass
from typing import List
from ...domain.entities.quote import Quote
from ...domain.repositories.i_extraction_repository import IExtractionRepository
from ...domain.repositories.i_tag_repository import ITagRepository


@dataclass
class CreateQuoteCommand:
    extraction_id: int
    text: str
    location: str
    user_id: int
    tag_ids: List[int]


class CreateQuoteHandler:
    def __init__(self, extraction_repo: IExtractionRepository, tag_repo: ITagRepository):
        self.extraction_repo = extraction_repo
        self.tag_repo = tag_repo

    def handle(self, command: CreateQuoteCommand):
        extraction = self.extraction_repo.get_by_id(command.extraction_id)
        if not extraction:
            raise ValueError("Extraction not found")

        # Validar que el usuario sea el asignado
        if extraction.assigned_to_user_id != command.user_id:
            raise ValueError("Unauthorized")

        # Construir entidad Quote
        tags = [self.tag_repo.get_by_id(tid) for tid in command.tag_ids]

        quote = Quote(
            id=None,
            text=command.text,
            location=command.location,
            researcher_id=command.user_id,
            tags=tags
        )

        # Agregar al agregado y guardar
        extraction.add_quote(quote)
        self.extraction_repo.save(extraction)
        return quote