from typing import Optional
from ..shared.exceptions import BusinessRuleViolation, ResourceNotFound
from .models import Tag


class TagValidator:
    """
    Encapsula las reglas de negocio puras para la gestión de Tags.
    No realiza consultas a servicios externos; valida el estado de las entidades.
    """

    @staticmethod
    def validate_tag_exists(tag: Optional[Tag], tag_id: int):
        if not tag:
            raise ResourceNotFound(f"Tag {tag_id} no encontrado.")

    @staticmethod
    def validate_tag_status(tag: Tag, expected_status: str):
        if tag.approval_status != expected_status:
            raise BusinessRuleViolation(
                f"El tag '{tag.name}' tiene estado {tag.approval_status}, se esperaba {expected_status}."
            )

    @staticmethod
    def validate_same_project_context(tag_a: Tag, tag_b: Tag):
        if tag_a.extraction_phase != tag_b.extraction_phase:
            raise BusinessRuleViolation("Los tags deben pertenecer a la misma fase de extracción/proyecto.")

    @staticmethod
    def validate_tag_is_approved(tag: Tag):
        if tag.approval_status != Tag.ApprovalStatus.APPROVED:
            raise BusinessRuleViolation(
                f"La operación requiere que el tag '{tag.name}' esté APROBADO."
            )