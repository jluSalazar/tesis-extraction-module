from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from .quote import Quote
from ..value_objects.extraction_status import ExtractionStatus
from ..exceptions.extraction_exceptions import ExtractionValidationError


@dataclass
class Extraction:
    """
    Aggregate Root.
    Representa el proceso de extracción de datos de un estudio (antes Paper).
    """
    id: Optional[int]
    study_id: int  # Referencia externa a 'studies' app
    assigned_to_user_id: Optional[int]
    status: ExtractionStatus
    quotes: List[Quote] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def start_working(self):
        if self.status != ExtractionStatus.PENDING:
            raise ExtractionValidationError("Solo se pueden iniciar extracciones pendientes.")
        self.status = ExtractionStatus.IN_PROGRESS
        self.started_at = datetime.now()

    def add_quote(self, quote: Quote):
        self.quotes.append(quote)

    def complete(self, missing_mandatory_tags: List[str]):
        """
        Intenta completar la extracción. Valida invariantes del dominio.
        """
        if not self.quotes:
            raise ExtractionValidationError("No se puede completar una extracción sin quotes.")

        if missing_mandatory_tags:
            raise ExtractionValidationError(
                f"Faltan tags obligatorios: {', '.join(missing_mandatory_tags)}"
            )

        self.status = ExtractionStatus.DONE
        self.completed_at = datetime.now()

    @property
    def is_active(self) -> bool:
        return self.status == ExtractionStatus.IN_PROGRESS