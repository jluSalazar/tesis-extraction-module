from typing import List, Optional
from ...domain.repositories.i_design_repository import IDesignRepository
from ...domain.dtos.design_dtos import ResearchQuestionDTO

# ⚠️ ZONA SUCIA: Importación de modelos de otra app
try:
    from apps.design.models import ResearchQuestion
except ImportError:
    ResearchQuestion = None


class DesignServiceAdapter(IDesignRepository):

    def get_question_by_id(self, question_id: int) -> Optional[ResearchQuestionDTO]:
        if not ResearchQuestion: return None

        try:
            # Usamos el ORM de Django
            q = ResearchQuestion.objects.get(pk=question_id)
            return self._to_dto(q)
        except ResearchQuestion.DoesNotExist:
            return None

    def get_questions_by_project(self, project_id: int) -> List[ResearchQuestionDTO]:
        if not ResearchQuestion: return []

        qs = ResearchQuestion.objects.filter(project_id=project_id)
        return [self._to_dto(q) for q in qs]

    def question_exists(self, question_id: int) -> bool:
        if not ResearchQuestion: return False
        return ResearchQuestion.objects.filter(pk=question_id).exists()

    def _to_dto(self, model_instance) -> ResearchQuestionDTO:
        """Helper privado para mapear Modelo -> DTO"""
        return ResearchQuestionDTO(
            id=model_instance.id,
            text=model_instance.text,
            project_id=model_instance.project_id
        )