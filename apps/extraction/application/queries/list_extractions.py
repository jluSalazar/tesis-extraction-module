from dataclasses import dataclass
from typing import List, Optional
from ...domain.repositories.i_extraction_repository import IExtractionRepository
from ...domain.entities.extraction import Extraction


@dataclass
class ListExtractionsQuery:
    user_id: Optional[int] = None
    study_id: Optional[int] = None


class ListExtractionsHandler:
    def __init__(self, repository: IExtractionRepository):
        self.repository = repository

    def handle(self, query: ListExtractionsQuery) -> List[Extraction]:
        # Nota: En una implementación real, esto debería soportar paginación
        if query.user_id:
            return self.repository.list_by_user(query.user_id)

        # Si el repo soporta filtrado por estudio, se llamaría aquí.
        # Por ahora devolvemos lista vacía o implementación base.
        return []