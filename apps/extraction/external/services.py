from typing import List, Optional
from datetime import datetime
from .interfaces import IDesignService
from .models import ResearchQuestion


class DesignService(IDesignService):
    """
    Servicio público de la app Design, retorna modelos de Django.
    MOCK MODE: Crea instancias de ResearchQuestion con datos simulados.
    """

    @staticmethod
    def get_question_details(question_id: int) -> Optional[ResearchQuestion]:
        if question_id == 999:
            return None

        # Retorna una instancia del modelo ResearchQuestion
        # Nota: En un proyecto real, esto sería `ResearchQuestion.objects.get(id=question_id)`
        return ResearchQuestion(
            id=question_id,
            question_text="¿Cómo afecta el TDD a la productividad en equipos pequeños?",
            project_id=1,
            created_at=datetime.now(),
        )

    @staticmethod
    def get_questions_by_project(project_id: int) -> List[ResearchQuestion]:
        return [
            ResearchQuestion(
                id=101,
                question_text="¿Cuáles son los principales retos de la migración a microservicios?",
                project_id=project_id,
                created_at=datetime.now(),
            ),
            ResearchQuestion(
                id=102,
                question_text="¿Qué métricas definen el éxito en Clean Architecture?",
                project_id=project_id,
                created_at=datetime.now(),
            )
        ]

    @staticmethod
    def question_exists(question_id: int) -> bool:
        return question_id != 999


from typing import Optional
from .models import Study
from .interfaces import IAcquisitionService

class AcquisitionService(IAcquisitionService):
    """
    Servicio público de la app Acquisition, retorna modelos de Django.
    MOCK MODE: Crea instancias de Study con datos simulados.
    """

    @staticmethod
    def get_study_details(study_id: int) -> Optional[Study]:
        if study_id == 999:
            return None

        # Retorna una instancia del modelo Study
        return Study(
            id=study_id,
            title=f"Estudio Simulado #{study_id}: Impacto de la IA en Legacy Code",
            publication_year=2024,
            project_id=1,
            authors="Dr. House, John Doe",
        )

    @staticmethod
    def exists(study_id: int) -> bool:
        return study_id != 999

    @staticmethod
    def get_project_id(study_id: int) -> Optional[int]:
        if study_id == 999:
            return None
        return 1

from typing import List, Optional
from datetime import datetime
from .models import Project
from .interfaces import IProjectService
from .dtos import ProjectMemberDTO, ProjectStageDTO

class ProjectService(IProjectService):
    """
    Servicio público de la app Projects, retorna modelos de Django y DTOs específicos.
    MOCK MODE: Crea instancias de Project con datos simulados.
    """

    @staticmethod
    def get_project_details(project_id: int) -> Optional[Project]:
        if project_id == 999:
            return None

        # Retorna una instancia del modelo Project
        return Project(
            id=project_id,
            name="Proyecto SLR: Modernización de Sistemas",
            description="Revisión sistemática sobre patrones de modernización.",
            # Asumimos que `owner_id` es un campo que existe internamente en el modelo
        )

    @staticmethod
    def exists(project_id: int) -> bool:
        return project_id != 999

    @staticmethod
    def is_member(project_id: int, user_id: int) -> bool:
        return user_id != -1

    @staticmethod
    def get_members(project_id: int) -> List[ProjectMemberDTO]:
        # Retorna DTOs ya que no hay un modelo de Django para miembros aquí
        return [
            ProjectMemberDTO(user_id=1, role="OWNER", joined_at=datetime.now()),
            ProjectMemberDTO(user_id=2, role="COLLABORATOR", joined_at=datetime.now()),
        ]

    @staticmethod
    def get_current_stage(project_id: int) -> Optional[ProjectStageDTO]:
        # Retorna DTO ya que no hay un modelo de Django para la etapa actual aquí
        return ProjectStageDTO(
            id=1,
            name="EXTRACTION",
            status="OPENED",
        )