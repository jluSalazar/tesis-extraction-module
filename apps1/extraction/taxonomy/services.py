from typing import Dict, List, Set
from django.db import transaction
from apps.design.services import DesignService
from .repositories import TagRepository
from .models import Tag
from ..shared.exceptions import ResourceNotFound, BusinessRuleViolation


class TagService:
    def __init__(self):
        self.repository = TagRepository()

    @transaction.atomic
    def create_tag(self, project_id: int, name: str, question_id: int = None, user_id: int = None) -> Tag:
        # 1. Validar existencia de la pregunta en el módulo externo (Design)
        if question_id:
            if not DesignService.question_exists(question_id):
                raise ResourceNotFound(f"ResearchQuestion {question_id} no existe.")

            # Regla de negocio: Si hay pregunta, es Deductivo y Obligatorio
            tag_type = Tag.TagType.DEDUCTIVE
            is_mandatory = True
        else:
            tag_type = Tag.TagType.INDUCTIVE
            is_mandatory = False

        # 2. Persistir vía repositorio
        try:
            return self.repository.create(
                project_id=project_id,
                name=name,
                question_id=question_id,
                created_by_id=user_id,
                type=tag_type,
                is_mandatory=is_mandatory
            )
        except Exception as e:
            raise BusinessRuleViolation(f"Error creando tag: {str(e)}")


    def get_tag_configuration_status(self, project_id: int) -> Dict[str, Any]:
        """
        Implementa la lógica del Escenario 1: Visibilidad de la lista.

        Regla: La lista es PÚBLICA (visible para researchers) solo si
        TODAS las preguntas de investigación (PIs) tienen al menos un tag asociado.
        """
        # 1. Obtener PIs del servicio externo (Design Module)
        pis_data = DesignService.get_questions_by_project(project_id)
        if not pis_data:
            # Si no hay preguntas, técnicamente no hay nada que cubrir.
            # Depende de la regla de negocio, asumimos que no es visible hasta definir PIs.
            return {"visibility": "No Pública", "missing_pis": [], "is_ready": False}

        all_pi_ids: Set[int] = {pi['id'] for pi in pis_data}

        # 2. Obtener Tags definidos en el proyecto actual
        project_tags = self.repository.list_by_project(project_id)

        # 3. Calcular PIs cubiertas (aquellas que tienen un tag con question_id)
        covered_pi_ids: Set[int] = {
            tag.question_id for tag in project_tags
            if tag.question_id is not None
        }

        # 4. Determinar Visibilidad
        missing_pis = all_pi_ids - covered_pi_ids
        is_public = len(missing_pis) == 0

        return {
            "visibility": "Pública" if is_public else "No Pública",
            "is_ready": is_public,
            "total_pis": len(all_pi_ids),
            "covered_pis": len(covered_pi_ids),
            "missing_pi_ids": list(missing_pis)
        }

    def get_mandatory_tags(self, project_id: int) -> List[Dict]:
        """Retorna la lista de tags que serán obligatorios."""
        tags = self.repository.get_mandatory_tags(project_id)
        return [{"id": t.id, "name": t.name, "question_id": t.question_id} for t in tags]