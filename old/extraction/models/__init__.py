"""
Importa todos los modelos en el orden correcto para evitar
importaciones circulares.

ORDEN IMPORTANTE:
1. Modelos sin dependencias (ExtractionPhase, ExtractionRecord)
2. Comment (no depende de Quote ni Tag)
3. Quote y Tag (pueden usar Comment via string reference)
4. ErrorHandler (depende de ExtractionRecord)
"""

from .configuration import ExtractionPhase
from .paper_extraction import PaperExtraction
from .comments import Comment
from .quotes import Quote
from .tags import Tag
from .error_handlers import ErrorHandler

__all__ = [
    'ExtractionPhase',
    'PaperExtraction',
    'Comment',
    'Quote',
    'Tag',
    'ErrorHandler',
]