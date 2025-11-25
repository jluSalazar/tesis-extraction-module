from typing import List, Dict, Any
from django.utils import timezone

from apps.acquisition.services import AcquisitionService
from apps.extraction.shared.exceptions import BusinessRuleViolation, ResourceNotFound
from apps.extraction.taxonomy.services import TagService
from .repositories import ExtractionRepository
from .models import ExtractionStatus, PaperExtraction


class ExtractionService:
    def __init__(self):
        self.extraction_repo = ExtractionRepository()
        self.tag_service = TagService()

    def initialize_extraction(self, study_id: int) -> Dict[str, Any]:
        """
        Crea un registro de extracción para un paper existente.
        """
        study_data = AcquisitionService.get_study_details(study_id)
        if not study_data:
            raise ResourceNotFound(f"Study {study_id} no encontrado en Acquisition.")

        existing = self.extraction_repo.get_by_study_id(study_id)
        if existing:
            return self._serialize(existing, study_data)

        extraction = self.extraction_repo.create_extraction(
            study_id=study_id,
            project_id=study_data['project_id']
        )

        return self._serialize(extraction, study_data)

    def get_extraction_progress(self, extraction_id: int) -> Dict[str, Any]:
        """
        Calcula qué falta para completar la extracción.
        """
        extraction = self.extraction_repo.get_by_id(extraction_id)
        if not extraction:
            raise ResourceNotFound("Extraction not found")

        mandatory_tags_objs = self.tag_service.repository.get_mandatory_tags(extraction.project_id)
        mandatory_map = {t.id: t.name for t in mandatory_tags_objs}
        mandatory_ids = set(mandatory_map.keys())

        used_tag_ids = set(
            extraction.quotes.values_list('tags__id', flat=True)
        )
        used_tag_ids.discard(None)  # Remover None si no hay tags

        missing_ids = mandatory_ids - used_tag_ids
        missing_names = [mandatory_map[mid] for mid in missing_ids]

        status_label = "Completo" if extraction.status == ExtractionStatus.DONE else "Pendiente"
        is_ready_to_complete = len(missing_ids) == 0 and extraction.quotes.exists()

        return {
            "status": status_label,
            "is_ready_to_complete": is_ready_to_complete,
            "mandatory_tags_count": len(mandatory_ids),
            "extracted_tags_count": len(used_tag_ids & mandatory_ids),
            "missing_tags": missing_names
        }

    def complete_extraction(self, extraction_id: int, user_id: int) -> PaperExtraction:
        """
        Intenta marcar una extracción como completada.
        """
        extraction = self.extraction_repo.get_by_id(extraction_id)
        if not extraction:
            raise ResourceNotFound("Extraction not found")

        progress = self.get_extraction_progress(extraction_id)

        if progress['missing_tags']:
            raise BusinessRuleViolation(
                f"No se puede completar. Faltan los siguientes tags obligatorios: {', '.join(progress['missing_tags'])}"
            )

        if not extraction.quotes.exists():
            raise BusinessRuleViolation("Debe extraer al menos una cita (Quote).")

        extraction.status = ExtractionStatus.DONE
        extraction.completed_at = timezone.now()

        return self.extraction_repo.save(extraction)

    def _serialize(self, extraction, study_data=None):
        if not study_data:
            study_data = AcquisitionService.get_study_details(extraction.study_id) or {}

        return {
            "id": extraction.id,
            "status": extraction.status,
            "study_title": study_data.get('title', 'Unknown'),
            "study_authors": study_data.get('authors', 'Unknown'),
            "quote_count": extraction.quotes.count()
        }