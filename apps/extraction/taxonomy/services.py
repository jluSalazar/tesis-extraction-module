from typing import Dict, List, Set, Any
from django.db import transaction

from .repositories import TagRepository
from .models import Tag
from ..planning.services import ExtractionPhaseService
from ..shared.exceptions import ResourceNotFound, BusinessRuleViolation
from .validations import TagValidator


class TagService:
    def __init__(self):
        self.repository = TagRepository()
        self.extraction_phase_service = ExtractionPhaseService()
        self.validator = TagValidator()

    @transaction.atomic
    def create_deductive_tag(self, extraction_phase_id: int, name: str, question_id: int = None,
                             user_id: int = None) -> Tag:
        """
        Crea un tag **deductivo** (predefinido o basado en una pregunta de investigación).

        Solo puede ser creado por el **dueño del proyecto**. Si se vincula a una pregunta
        de investigación (`question_id`), el tag se marca automáticamente como **obligatorio**
        (`is_mandatory=True`).
        """
        phase = self.extraction_phase_service.get_phase_by_id(extraction_phase_id)
        if not phase:
            raise ResourceNotFound(f"Fase de extracción {extraction_phase_id} no encontrada.")

        if not self.extraction_phase_service.is_project_owner(user_id, phase.extraction_phase):
            raise BusinessRuleViolation(f"El usuario {user_id} no es el dueño del proyecto.")

        if question_id:
            if not self.extraction_phase_service.question_belongs_to_project(question_id, phase.extraction_phase):
                raise BusinessRuleViolation(f"La pregunta {question_id} no pertenece al proyecto actual.")
            is_mandatory = True
        else:
            is_mandatory = False

        try:
            return self.repository.create(
                extraction_phase_id=extraction_phase_id,
                name=name,
                question_id=question_id,
                created_by_id=user_id,
                type=Tag.TagType.DEDUCTIVE,
                is_mandatory=is_mandatory,
                is_public=True,
                approval_status=Tag.ApprovalStatus.APPROVED
            )
        except Exception as e:
            raise BusinessRuleViolation(f"Error creando tag deductivo: {str(e)}")

    @transaction.atomic
    def create_inductive_tag(self, extraction_phase_id: int, name: str, user_id: int) -> Tag:
        """
        Crea un tag **inductivo** generado por un investigador durante la extracción.

        Estos tags son **privados** (`is_public=False`) y tienen un estado de aprobación **PENDIENTE**
        (`ApprovalStatus.PENDING`), requiriendo revisión por el dueño del proyecto.
        """
        try:
            return self.repository.create(
                extraction_phase_id=extraction_phase_id,
                name=name,
                question_id=None,
                created_by_id=user_id,
                type=Tag.TagType.INDUCTIVE,
                is_mandatory=False,
                is_public=False,
                approval_status=Tag.ApprovalStatus.PENDING
            )
        except Exception as e:
            raise BusinessRuleViolation(f"Error creando tag inductivo: {str(e)}")

    def approve_tag(self, tag_id: int, owner_id: int) -> Tag:
        """
        Aprueba un tag que está en estado PENDIENTE.

        Solo el dueño del proyecto puede realizar esta acción. Al ser aprobado, el tag
        se convierte en **público** (`is_public=True`) y está disponible para todos los investigadores.
        """
        tag = self.repository.get_by_id(tag_id)
        self.validator.validate_tag_exists(tag, tag_id)

        phase = tag.extraction_phase

        if not self.extraction_phase_service.is_project_owner(owner_id, phase.project_id):
            raise BusinessRuleViolation("Solo el dueño del proyecto puede aprobar tags.")

        self.validator.validate_tag_status(tag, Tag.ApprovalStatus.PENDING)

        tag.approval_status = Tag.ApprovalStatus.APPROVED
        tag.is_public = True

        return self.repository.save(tag)

    def reject_tag(self, tag_id: int, owner_id: int) -> Tag:
        """
        Rechaza un tag que está en estado PENDIENTE.

        Solo el dueño del proyecto puede realizar esta acción. El tag permanece **no público**
        (`is_public=False`) y no puede ser usado por otros investigadores.
        """
        tag = self.repository.get_by_id(tag_id)
        self.validator.validate_tag_exists(tag, tag_id)

        phase = tag.extraction_phase

        if not self.extraction_phase_service.is_project_owner(owner_id, phase.project_id):
            raise BusinessRuleViolation("Solo el dueño del proyecto puede rechazar tags.")

        self.validator.validate_tag_status(tag, Tag.ApprovalStatus.PENDING)

        tag.approval_status = Tag.ApprovalStatus.REJECTED
        tag.is_public = False

        return self.repository.save(tag)

    @transaction.atomic
    def merge_tags(self, approved_tag_id: int, duplicate_tag_id: int, owner_id: int) -> Tag:
        """
        Fusiona un tag duplicado en un tag aprobado existente.

        Solo el dueño del proyecto puede realizar esta acción. Todas las citas (Quotes)
        asociadas al tag duplicado (`duplicate_tag_id`) serán reasignadas al tag aprobado
        (`approved_tag_id`), y el tag duplicado será marcado como obsoleto/eliminado.
        """
        approved_tag = self.repository.get_by_id(approved_tag_id)
        duplicate_tag = self.repository.get_by_id(duplicate_tag_id)

        self.validator.validate_tag_exists(approved_tag, approved_tag_id)
        self.validator.validate_tag_exists(duplicate_tag, duplicate_tag_id)

        phase = approved_tag.extraction_phase

        if not self.extraction_phase_service.is_project_owner(owner_id, phase.project_id):
            raise BusinessRuleViolation("Permiso denegado para fusionar tags.")

        self.validator.validate_same_project_context(approved_tag, duplicate_tag)
        self.validator.validate_tag_is_approved(approved_tag)

        return self.repository.merge_tags(duplicate_tag, approved_tag)

    def link_tag_to_question(self, tag_id: int, question_id: int, owner_id: int) -> Tag:
        """
        Vincula un tag (generalmente uno aprobado inductivamente) a una pregunta de investigación (PI).

        Solo el dueño del proyecto puede realizar esta acción. El tag debe estar previamente
        aprobado. Al vincularse, se convierte en tipo **Deductivo** y se marca como **Obligatorio**
        (`is_mandatory=True`).
        """
        tag = self.repository.get_by_id(tag_id)
        self.validator.validate_tag_exists(tag, tag_id)

        phase = tag.extraction_phase

        if not self.extraction_phase_service.is_project_owner(owner_id, phase.project_id):
            raise BusinessRuleViolation("Permiso denegado para vincular tags.")

        self.validator.validate_tag_is_approved(tag)

        if not self.extraction_phase_service.question_belongs_to_project(question_id, phase.project_id):
            raise BusinessRuleViolation(f"La pregunta {question_id} no pertenece al proyecto.")

        tag.question_id = question_id
        tag.type = Tag.TagType.DEDUCTIVE
        tag.is_mandatory = True

        return self.repository.save(tag)

    # =========================================================================
    # Reportes y Getters
    # =========================================================================

    def get_tag_configuration_status(self, project_id: int) -> Dict[str, Any]:
        """
        Obtiene el estado de la configuración de tags obligatorios (cobertura de PI).

        Verifica si todas las Preguntas de Investigación (PI) del proyecto han sido
        cubiertas por tags que están vinculados a ellas y han sido aprobados.
        """
        pis_data = self.extraction_phase_service.get_project_research_questions(project_id)

        if not pis_data:
            return {"visibility": "No Pública", "missing_pis": [], "is_ready": False}

        all_pi_ids: Set[int] = {pi['id'] for pi in pis_data}

        extraction_phase = self.extraction_phase_service.get_or_create_phase(project_id)

        all_tags = self.repository.list_by_project(extraction_phase.id)

        covered_pi_ids: Set[int] = {
            tag.question_id for tag in all_tags
            if tag.question_id is not None and tag.approval_status == Tag.ApprovalStatus.APPROVED
        }

        missing_pis = all_pi_ids - covered_pi_ids
        is_public = len(missing_pis) == 0

        return {
            "visibility": "Pública" if is_public else "No Pública",
            "is_ready": is_public,
            "total_pis": len(all_pi_ids),
            "covered_pis": len(covered_pi_ids),
            "missing_pi_ids": list(missing_pis)
        }

    def get_visible_tags_for_user(self, extraction_phase_id: int, user_id: int) -> List[Tag]:
        """
        Obtiene la lista de tags que son visibles para un investigador específico.

        Incluye tags públicos (deductivos o inductivos aprobados) y tags privados
        creados por el propio investigador.
        """
        return self.repository.get_tags_for_user(extraction_phase_id, user_id)

    def get_mandatory_tags(self, extraction_phase_id: int) -> List[Tag]:
        """
        Obtiene todos los tags marcados como obligatorios (`is_mandatory=True`)
        para una fase de extracción.
        """
        return self.repository.get_mandatory_tags(extraction_phase_id)

    def get_pending_tags_for_owner(self, extraction_phase_id: int) -> List[Tag]:
        """
        Obtiene todos los tags que están en estado **PENDIENTE** de aprobación,
        típicamente tags inductivos, para la revisión del dueño del proyecto.
        """
        return self.repository.get_pending_tags(extraction_phase_id)

    def get_tags_statistics(self, extraction_phase_id: int) -> Dict[str, Any]:
        """
        Calcula estadísticas de uso y estado de los tags en una fase de extracción.
        (Ej. conteo de tags inductivos, deductivos, aprobados, rechazados, etc.)
        """
        all_tags = self.repository.list_by_project(extraction_phase_id)
        # ... lógica de conteo ...
        return {}

    def get_tags_organized_for_researcher(self, extraction_phase_id: int, user_id: int) -> Dict[str, List[Tag]]:
        """
        Obtiene los tags visibles para un investigador organizados en categorías:
        Obligatorios, Opcionales Públicos y Privados (creados por el usuario).
        """
        user_tags = self.repository.get_tags_for_user(extraction_phase_id, user_id)
        result = {"mandatory": [], "optional_public": [], "private": []}
        for tag in user_tags:
            if tag.is_mandatory:
                result["mandatory"].append(tag)
            elif tag.is_public and tag.approval_status == Tag.ApprovalStatus.APPROVED:
                result["optional_public"].append(tag)
            elif tag.created_by_id == user_id:
                result["private"].append(tag)
        return result