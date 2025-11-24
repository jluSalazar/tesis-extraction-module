
# ================================================
# FILE: extraction/services/validation_service.py
# ================================================
"""Servicio para validaciones de reglas de negocio."""

from typing import List
from old.extraction.models import Tag, PaperExtraction
from projects.models import ResearchProject
from design.models import ResearchQuestion


class ValidationService:
    """
    Encapsula validaciones complejas de reglas de negocio.

    Responsabilidades:
    - Verificar visibilidad de listas
    - Validar completitud de extracciones
    - Verificar tags obligatorios
    """

    @staticmethod
    def is_tag_list_public(project: ResearchProject) -> bool:
        """
        Determina si la lista de tags debe ser visible para Researchers.

        Regla de Negocio #9:
        "La lista de tags será visible siempre y cuando TODAS las
         preguntas de investigación estén siendo usadas por un tag."

        Lógica:
        - Si TODAS las PIs tienen al menos 1 tag → Lista VISIBLE
        - Si ALGUNA PI no tiene tags → Lista OCULTA

        Args:
            project: Proyecto a verificar

        Returns:
            bool: True si la lista debe ser pública, False si no
        """
        # Buscar PIs sin tags asociados
        pis_without_tags = ResearchQuestion.objects.filter(
            project=project,
            tags__isnull=True
        ).exists()

        # Si existe alguna PI sin tags → Lista NO pública
        return not pis_without_tags

    @staticmethod
    def get_missing_mandatory_tags(
            paper_extraction: PaperExtraction
    ) -> List[Tag]:
        """
        Retorna los tags obligatorios que faltan en una extracción.

        Regla de Negocio #12:
        "Un paper solo puede marcarse como 'Completo' si todas las
         extracciones obligatorias han sido registradas."

        Args:
            paper_extraction: Extracción a verificar

        Returns:
            List[Tag]: Lista de tags obligatorios faltantes
        """
        project = paper_extraction.project

        # Obtener todos los tags obligatorios del proyecto
        mandatory_tags = Tag.objects.filter(
            question__project=project,
            is_mandatory=True
        )

        # Obtener tags que YA están en quotes de esta extracción
        used_tags = Tag.objects.filter(
            quotes__paper_extraction=paper_extraction
        ).distinct()

        # Tags faltantes = obligatorios - usados
        missing_tags = mandatory_tags.exclude(
            id__in=used_tags.values_list('id', flat=True)
        )

        return list(missing_tags)

    @staticmethod
    def can_complete_extraction(
            paper_extraction: PaperExtraction
    ) -> tuple[bool, str]:
        """
        Verifica si una extracción puede marcarse como completada.

        Reglas de Negocio:
        - Debe tener al menos una quote (Regla #17)
        - No debe tener tags obligatorios faltantes (Regla #12)
        - No debe tener errores sin resolver

        Returns:
            tuple: (puede_completar: bool, mensaje: str)
        """
        # Verificar que tenga quotes
        if not paper_extraction.has_quotes:
            return False, "La extracción no tiene quotes registradas"

        # Verificar tags obligatorios
        missing_tags = ValidationService.get_missing_mandatory_tags(
            paper_extraction
        )

        if missing_tags:
            tag_names = [tag.name for tag in missing_tags]
            return False, f"Faltan tags obligatorios: {', '.join(tag_names)}"

        # Verificar errores sin resolver
        if paper_extraction.has_errors:
            return False, "Existen errores sin resolver en la extracción"

        return True, "La extracción puede ser completada"

