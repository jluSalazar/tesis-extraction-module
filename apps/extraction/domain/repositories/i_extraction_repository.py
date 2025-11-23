from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.extraction import Extraction


class IExtractionRepository(ABC):
    @abstractmethod
    def get_by_id(self, extraction_id: int) -> Optional[Extraction]:
        pass

    @abstractmethod
    def get_by_study_id(self, study_id: int) -> Optional[Extraction]:
        pass

    @abstractmethod
    def save(self, extraction: Extraction) -> Extraction:
        """Persiste la entidad y retorna la versión actualizada (con ID)"""
        pass

    @abstractmethod
    def list_by_user(self, user_id: int, include_quotes: bool = False) -> List[Extraction]:
        pass