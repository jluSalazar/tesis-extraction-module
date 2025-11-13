
# ================================================
# FILE: extraction/exceptions.py
# ================================================
"""Excepciones personalizadas para la app extraction."""
from typing import List


class ExtractionException(Exception):
    """Base exception para la app extraction."""
    pass


class TagValidationError(ExtractionException):
    """Error de validación en Tags."""
    pass


class QuoteValidationError(ExtractionException):
    """Error de validación en Quotes."""
    pass


class ExtractionPhaseClosedError(ExtractionException):
    """Intento de operación en fase cerrada."""
    pass


class MissingMandatoryTagsError(ExtractionException):
    """Faltan tags obligatorios."""

    def __init__(self, missing_tags: List):
        self.missing_tags = missing_tags
        tag_names = [tag.name for tag in missing_tags]
        super().__init__(
            f"Faltan tags obligatorios: {', '.join(tag_names)}"
        )