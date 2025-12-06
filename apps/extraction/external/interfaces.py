from abc import ABC, abstractmethod
from typing import List, Optional

from .models import Project, ResearchQuestion, Study

from .dtos import ProjectMemberDTO, ProjectStageDTO

# --- INTERFACES ---

class IDesignService(ABC):
    """Interfaz (Puerto) para obtener información del dominio Diseño."""

    @abstractmethod
    def get_question_details(self, question_id: int) -> Optional[ResearchQuestion]: # Retorna Modelo
        """Obtiene una pregunta por ID, retornando el modelo ResearchQuestion."""
        pass

    @abstractmethod
    def get_questions_by_project(self, project_id: int) -> List[ResearchQuestion]: # Retorna Modelo
        """Obtiene todas las preguntas de un proyecto, retornando una lista de modelos."""
        pass

    @abstractmethod
    def question_exists(self, question_id: int) -> bool:
        """Verifica la existencia de la pregunta."""
        pass


class IAcquisitionService(ABC):
    """Interfaz (Puerto) para obtener información del dominio Adquisición."""

    @abstractmethod
    def get_study_details(self, study_id: int) -> Optional[Study]: # Retorna Modelo
        """Obtiene detalles de un estudio, retornando el modelo Study."""
        pass

    @abstractmethod
    def exists(self, study_id: int) -> bool:
        """Verifica la existencia del estudio."""
        pass

    @abstractmethod
    def get_project_id(self, study_id: int) -> Optional[int]:
        """Obtiene el ID del proyecto al que pertenece el estudio."""
        pass


class IProjectService(ABC):
    """Interfaz (Puerto) para obtener información del dominio Proyecto."""

    @abstractmethod
    def get_project_details(self, project_id: int) -> Optional[Project]: # Retorna Modelo
        """Obtiene detalles del proyecto, retornando el modelo Project."""
        pass

    @abstractmethod
    def exists(self, project_id: int) -> bool:
        """Verifica la existencia del proyecto."""
        pass

    @abstractmethod
    def is_member(self, project_id: int, user_id: int) -> bool:
        """Verifica si un usuario es miembro del proyecto."""
        pass

    @abstractmethod
    def get_members(self, project_id: int) -> List[ProjectMemberDTO]: # Retorna DTO
        """Obtiene la lista de miembros."""
        pass

    @abstractmethod
    def get_current_stage(self, project_id: int) -> Optional[ProjectStageDTO]: # Retorna DTO
        """Obtiene la etapa actual del proyecto."""
        pass