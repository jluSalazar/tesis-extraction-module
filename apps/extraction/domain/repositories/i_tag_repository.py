from abc import ABC, abstractmethod
from typing import List
from ..entities.tag import Tag


class ITagRepository(ABC):
    """Puerto para acceder a los tags (que podrían venir de otra app 'design')."""

    @abstractmethod
    def get_by_id(self, tag_id: int) -> Tag:
        pass

    @abstractmethod
    def get_mandatory_tags_for_project_context(self, study_id: int) -> List[Tag]:
        """
        Obtiene los tags obligatorios asociados al proyecto de un estudio.
        Nota: Recibe study_id porque la capa de extracción no conoce 'Project',
        el adaptador deberá resolver esa relación.
        """
        pass