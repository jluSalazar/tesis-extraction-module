from typing import Dict, List, Set, Any, Optional
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
        """
        Crea un tag deductivo (vinculado a PI) u opcional.
        Los tags deductivos son automáticamente obligatorios y públicos.
        """
        # 1. Validar existencia de la pregunta en el módulo externo (Design)
        if question_id:
            if not DesignService.question_exists(question_id):
                raise ResourceNotFound(f"ResearchQuestion {question_id} no existe.")

            # Regla de negocio: Si hay pregunta, es Deductivo y Obligatorio
            tag_type = Tag.TagType.DEDUCTIVE
            is_mandatory = True
            is_public = True
            approval_status = Tag.ApprovalStatus.APPROVED
        else:
            # Tag sin PI - es opcional pero público
            tag_type = Tag.TagType.DEDUCTIVE
            is_mandatory = False
            is_public = True
            approval_status = Tag.ApprovalStatus.APPROVED

        # 2. Persistir vía repositorio
        try:
            return self.repository.create(
                project_id=project_id,
                name=name,
                question_id=question_id,
                created_by_id=user_id,
                type=tag_type,
                is_mandatory=is_mandatory,
                is_public=is_public,
                approval_status=approval_status
            )
        except Exception as e:
            raise BusinessRuleViolation(f"Error creando tag: {str(e)}")

    @transaction.atomic
    def create_inductive_tag(self, project_id: int, name: str, user_id: int) -> Tag:
        """
        Crea un tag inductivo para uso personal del investigador.
        - Estado: Pendiente de Aprobación
        - Visibilidad: Privada (solo visible para el creador)
        - Tipo: Inductivo
        """
        try:
            return self.repository.create(
                project_id=project_id,
                name=name,
                question_id=None,  # Tags inductivos no se vinculan a PIs
                created_by_id=user_id,
                type=Tag.TagType.INDUCTIVE,
                is_mandatory=False,
                is_public=False,  # Privado hasta aprobación
                approval_status=Tag.ApprovalStatus.PENDING
            )
        except Exception as e:
            raise BusinessRuleViolation(f"Error creando tag inductivo: {str(e)}")

    def approve_tag(self, tag_id: int, owner_id: int) -> Tag:
        """
        Owner aprueba un tag propuesto.
        - Cambia estado a Aprobado
        - Cambia visibilidad a Pública
        """
        tag = self.repository.get_by_id(tag_id)
        if not tag:
            raise ResourceNotFound(f"Tag {tag_id} no encontrado.")

        if tag.approval_status != Tag.ApprovalStatus.PENDING:
            raise BusinessRuleViolation(f"El tag no está pendiente de aprobación.")

        tag.approval_status = Tag.ApprovalStatus.APPROVED
        tag.is_public = True

        return self.repository.save(tag)

    def reject_tag(self, tag_id: int, owner_id: int) -> Tag:
        """
        Owner rechaza un tag propuesto.
        - Cambia estado a Rechazado
        - Mantiene visibilidad Privada (solo útil para el creador original)
        """
        tag = self.repository.get_by_id(tag_id)
        if not tag:
            raise ResourceNotFound(f"Tag {tag_id} no encontrado.")

        if tag.approval_status != Tag.ApprovalStatus.PENDING:
            raise BusinessRuleViolation(f"El tag no está pendiente de aprobación.")

        tag.approval_status = Tag.ApprovalStatus.REJECTED
        tag.is_public = False  # Sigue siendo privado

        return self.repository.save(tag)

    @transaction.atomic
    def merge_tags(self, approved_tag_id: int, duplicate_tag_id: int, owner_id: int) -> Tag:
        """
        Fusiona un tag duplicado en el tag aprobado.
        - Reasigna todas las extracciones del duplicado al aprobado
        - Marca el duplicado como fusionado
        """
        approved_tag = self.repository.get_by_id(approved_tag_id)
        duplicate_tag = self.repository.get_by_id(duplicate_tag_id)

        if not approved_tag:
            raise ResourceNotFound(f"Tag aprobado {approved_tag_id} no encontrado.")
        if not duplicate_tag:
            raise ResourceNotFound(f"Tag duplicado {duplicate_tag_id} no encontrado.")

        if approved_tag.project_id != duplicate_tag.project_id:
            raise BusinessRuleViolation("Los tags deben pertenecer al mismo proyecto.")

        # El tag aprobado debe estar aprobado
        if approved_tag.approval_status != Tag.ApprovalStatus.APPROVED:
            raise BusinessRuleViolation("El tag destino debe estar aprobado.")

        return self.repository.merge_tags(duplicate_tag, approved_tag)

    def get_visible_tags_for_user(self, project_id: int, user_id: int) -> List[Dict]:
        """
        Lista de tags visibles para un usuario específico:
        - Tags públicos y aprobados (de cualquier creador)
        - Tags privados propios (cualquier estado)
        """
        tags = self.repository.get_tags_for_user(project_id, user_id)
        return [self._serialize_tag(t) for t in tags]

    def get_tag_configuration_status(self, project_id: int) -> Dict[str, Any]:
        """
        Implementa la lógica del Escenario 1: Visibilidad de la lista.

        Regla: La lista es PÚBLICA (visible para researchers) solo si
        TODAS las preguntas de investigación (PIs) tienen al menos un tag asociado.
        """
        # 1. Obtener PIs del servicio externo (Design Module)
        pis_data = DesignService.get_questions_by_project(project_id)
        if not pis_data:
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

    def get_mandatory_tag_names(self, project_id: int) -> List[str]:
        """Retorna solo los nombres de tags obligatorios."""
        tags = self.repository.get_mandatory_tags(project_id)
        return [t.name for t in tags]

    def _serialize_tag(self, tag: Tag) -> Dict:
        """Serializa un tag a diccionario"""
        return {
            "id": tag.id,
            "name": tag.name,
            "type": tag.type,
            "is_mandatory": tag.is_mandatory,
            "is_public": tag.is_public,
            "approval_status": tag.approval_status,
            "question_id": tag.question_id,
            "created_by_id": tag.created_by_id
        }