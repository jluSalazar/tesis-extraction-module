
# ================================================
# FILE: extraction/services/tag_service.py
# ================================================
"""Servicio para gestión de Tags."""

from typing import Optional
from django.db import transaction
from django.core.exceptions import ValidationError

from old.extraction.models import Tag
from old.extraction.exceptions import TagValidationError
from projects.models import ResearchProject
from design.models import ResearchQuestion


class TagService:
    """
    Encapsula toda la lógica de negocio relacionada con Tags.

    Responsabilidades:
    - Creación de tags (deductivos e inductivos)
    - Actualización de tags
    - Validación de reglas de negocio
    - Eliminación segura
    """

    @staticmethod
    @transaction.atomic
    def create_tag(
            creator,
            project: ResearchProject,
            name: str,
            question: Optional[ResearchQuestion] = None,
            color: str = '#FFFFFF',
            justification: str = ''
    ) -> Tag:
        """
        Crea un Tag aplicando reglas de negocio.

        Reglas de Negocio Aplicadas:
        - Si tiene 'question' → is_mandatory=True (Regla #10)
        - Si no tiene 'question' → is_mandatory=False (Regla #11)
        - Si tiene 'question' → type=DEDUCTIVE
        - Si no tiene 'question' → type=INDUCTIVE

        Args:
            creator: Usuario que crea el tag (Owner o Researcher)
            project: Proyecto al que pertenece
            name: Nombre del tag
            question: PI asociada (None para tags inductivos)
            color: Color hexadecimal para visualización
            justification: Definición y criterios de aplicación

        Returns:
            Tag: El tag creado

        Raises:
            TagValidationError: Si hay errores de validación
        """
        # Validación: No duplicar tags con el mismo nombre en el mismo proyecto
        if question:
            # Para tags deductivos: nombre único por proyecto + pregunta
            existing = Tag.objects.filter(
                name=name,
                question=question
            ).exists()

            if existing:
                raise TagValidationError(
                    f"Ya existe un tag '{name}' vinculado a la pregunta '{question.text}'"
                )

        # Determinar tipo y obligatoriedad según la PI
        tag_type = Tag.TagType.DEDUCTIVE if question else Tag.TagType.INDUCTIVE
        is_mandatory = question is not None

        # Crear el tag
        tag = Tag.objects.create(
            name=name,
            color=color,
            justification=justification,
            created_by=creator,
            question=question,
            type=tag_type,
            is_mandatory=is_mandatory,
            is_public=True
        )

        return tag

    @staticmethod
    @transaction.atomic
    def update_tag(
            tag: Tag,
            name: Optional[str] = None,
            color: Optional[str] = None,
            justification: Optional[str] = None,
            question: Optional[ResearchQuestion] = None,
            is_public: Optional[bool] = None
    ) -> Tag:
        """
        Actualiza un Tag aplicando reglas de negocio.

        IMPORTANTE: Si se cambia 'question', se recalcula automáticamente
        'is_mandatory' y 'type' según las reglas de negocio.
        """
        # Actualizar campos simples
        if name is not None:
            tag.name = name
        if color is not None:
            tag.color = color
        if justification is not None:
            tag.justification = justification
        if is_public is not None:
            tag.is_public = is_public

        # Actualizar question y recalcular dependencias
        if question is not None:
            tag.question = question
            tag.is_mandatory = True
            tag.type = Tag.TagType.DEDUCTIVE
        elif question is None and 'question' in locals():
            # Se pasó explícitamente None para desvincularlo
            tag.question = None
            tag.is_mandatory = False
            tag.type = Tag.TagType.INDUCTIVE

        tag.save()
        return tag

    @staticmethod
    def can_delete_tag(tag: Tag) -> tuple[bool, str]:
        """
        Verifica si un tag puede ser eliminado.

        Reglas:
        - No se puede eliminar si tiene quotes asociadas

        Returns:
            tuple: (puede_eliminar: bool, mensaje: str)
        """
        if tag.quotes.exists():
            quote_count = tag.quotes.count()
            return False, f"No se puede eliminar. Tiene {quote_count} quote(s) asociada(s)"

        return True, "El tag puede ser eliminado"

    @staticmethod
    @transaction.atomic
    def delete_tag(tag: Tag) -> None:
        """
        Elimina un tag de forma segura.

        Raises:
            ValidationError: Si el tag no puede ser eliminado
        """
        can_delete, message = TagService.can_delete_tag(tag)

        if not can_delete:
            raise ValidationError(message)

        tag.delete()

