from typing import List, Dict, Any, Optional
from django.utils import timezone
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
import logging

from apps.extraction.shared.exceptions import BusinessRuleViolation, ResourceNotFound
from apps.extraction.taxonomy.services import TagService
from apps.extraction.taxonomy.repositories import TagRepository
from apps.extraction.planning.services import ExtractionPhaseService # Único punto de contacto

from .repositories import ExtractionRepository
from .models import ExtractionStatus, PaperExtraction, Quote, Comment


logger = logging.getLogger(__name__)
#TODO crear un dto para la informacion necesaria para el front
class ExtractionService:
    def __init__(self):
        self.extraction_repo = ExtractionRepository()
        self.tag_service = TagService()
        self.tag_repo = TagRepository()
        self.phase_service = ExtractionPhaseService()

    def initialize_extraction(self, study_id: int, project_id: int) -> Dict[str, Any]:
        """
        Crea o recupera un registro de extracción.
        Requiere comunicarse con el PhaseService para validar el paper.
        """
        study_data = self.phase_service.get_paper_metadata(study_id)
        if not study_data:
            raise ResourceNotFound(f"Study {study_id} no encontrado o no pertenece al proyecto.")

        existing = self.extraction_repo.get_by_study_id(study_id)
        if existing:
            return self._serialize_extraction_with_meta(existing, study_data)

        phase = self.phase_service.get_or_create_phase(project_id)

        extraction = self.extraction_repo.create_extraction(
            study_id=study_id,
            extraction_phase_id=phase.id
        )

        return self._serialize_extraction_with_meta(extraction, study_data)

    def get_extraction_by_study(self, study_id: int) -> PaperExtraction:
        """Obtiene la extracción por study_id"""
        extraction = self.extraction_repo.get_by_study_id(study_id)
        if not extraction:
            raise ResourceNotFound(f"No existe extracción para el study {study_id}")
        return extraction

    def get_extraction_progress(self, extraction_id: int) -> Dict[str, Any]:
        """Calcula métricas de completitud."""
        extraction = self.extraction_repo.get_by_id(extraction_id)
        if not extraction:
            raise ResourceNotFound("Extraction not found")

        mandatory_tags = self.tag_service.get_mandatory_tags(extraction.extraction_phase_id)
        mandatory_ids = {t.id for t in mandatory_tags}
        mandatory_names_map = {t.id: t.name for t in mandatory_tags}

        used_ids = set(
            extraction.quotes.values_list('tags__id', flat=True)
        )
        used_ids.discard(None)

        missing_ids = mandatory_ids - used_ids
        missing_names = [mandatory_names_map[mid] for mid in missing_ids]

        is_ready = len(missing_ids) == 0 and extraction.quotes.exists()

        return {
            "status": extraction.get_status_display(),
            "status_code": extraction.status,
            "is_ready_to_complete": is_ready,
            "mandatory_total": len(mandatory_ids),
            "mandatory_covered": len(mandatory_ids) - len(missing_ids),
            "missing_tags": missing_names
        }

    @transaction.atomic
    def create_quote(self, extraction_id: int, researcher_id: int,
                     text_portion: str, location: str = "",
                     tag_names: List[str] = None,
                     new_inductive_tag: str = None) -> Quote:

        extraction = self.extraction_repo.get_by_id(extraction_id)
        if not extraction:
            raise ResourceNotFound("Extraction not found")

        if not self.phase_service.is_researcher_assigned_to_paper(extraction.study_id, researcher_id,
                                                                  extraction.extraction_phase_id):
            raise BusinessRuleViolation("El investigador no está asignado a este paper.")

        quote = Quote.objects.create(
            paper_extraction=extraction,
            text_portion=text_portion,
            location=location,
            researcher_id=researcher_id
        )

        if tag_names:
            user_tags = self.tag_repo.get_tags_for_user(extraction.extraction_phase_id, researcher_id)
            tag_map = {t.name: t for t in user_tags}

            tags_to_add = []
            for name in tag_names:
                if name in tag_map:
                    tags_to_add.append(tag_map[name])

            if tags_to_add:
                quote.tags.add(*tags_to_add)

        if new_inductive_tag:
            new_tag = self.tag_service.create_inductive_tag(
                extraction_phase_id=extraction.extraction_phase_id,
                name=new_inductive_tag,
                user_id=researcher_id
            )
            quote.tags.add(new_tag)

        # Actualizar estado si es necesario
        if extraction.status == ExtractionStatus.PENDING:
            extraction.status = ExtractionStatus.IN_PROGRESS
            self.extraction_repo.save(extraction)

        return quote

    def add_comment_to_quote(self, quote_id: int, user_id: int, text: str) -> Comment:
        """Agrega un comentario a una quote"""
        try:
            quote = Quote.objects.get(id=quote_id)
        except Quote.DoesNotExist:
            raise ResourceNotFound("Quote not found")

        content_type = ContentType.objects.get_for_model(Quote)

        comment = Comment.objects.create(
            user_id=user_id,
            text=text,
            content_type=content_type,
            object_id=quote_id
        )

        return comment

    def get_quote_comments(self, quote_id: int) -> List[Dict[str, Any]]:
        """Obtiene los comentarios de una quote"""
        try:
            quote = Quote.objects.get(id=quote_id)
        except Quote.DoesNotExist:
            raise ResourceNotFound("Quote not found")

        content_type = ContentType.objects.get_for_model(Quote)
        comments = Comment.objects.filter(
            content_type=content_type,
            object_id=quote_id
        ).order_by('created_at')

        return [{
            "id": c.id,
            "text": c.text,
            "user_id": c.user_id,
            "created_at": c.created_at.isoformat()
        } for c in comments]

    def get_quotes_by_extraction(self, extraction_id: int) -> List[Dict[str, Any]]:
        """Obtiene todas las quotes de una extracción"""
        extraction = self.extraction_repo.get_by_id(extraction_id)
        if not extraction:
            raise ResourceNotFound("Extraction not found")

        quotes = extraction.quotes.prefetch_related('tags').all()

        return [{
            "id": q.id,
            "text_portion": q.text_portion,
            "location": q.location,
            "tags": [{"id": t.id, "name": t.name} for t in q.tags.all()],
            "researcher_id": q.researcher_id,
            "validated": q.validated,
            "created_at": q.created_at.isoformat()
        } for q in quotes]

    def complete_extraction(self, extraction_id: int, user_id: int) -> PaperExtraction:
        extraction = self.extraction_repo.get_by_id(extraction_id)
        if not extraction:
            raise ResourceNotFound("Extraction not found")

        progress = self.get_extraction_progress(extraction_id)

        if not progress['is_ready_to_complete']:
            missing = ", ".join(progress['missing_tags'])
            raise BusinessRuleViolation(f"Faltan tags obligatorios: {missing}")

        extraction.status = ExtractionStatus.DONE
        extraction.completed_at = timezone.now()

        return self.extraction_repo.save(extraction)

    def get_researcher_papers(self, project_id: int, researcher_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene papers asignados al researcher.
        Flujo:
        1. Pide assignments y metadatos a ExtractionPhaseService.
        2. Cruza con la DB local de PaperExtraction para saber el estado y progreso.
        """
        assigned_studies = self.phase_service.get_assigned_papers_details(project_id, researcher_id)

        if not assigned_studies:
            return []

        study_ids = [s['id'] for s in assigned_studies]

        local_extractions = {
            ext.study_id: ext
            for ext in PaperExtraction.objects.filter(study_id__in=study_ids)
        }

        result = []
        for study in assigned_studies:
            study_id = study['id']
            extraction = local_extractions.get(study_id)

            item = {
                "id": study_id,
                "study_id": study_id,
                "title": study['title'],
                "authors": study['authors'],
                "pdf_url": study.get('pdf_url', '#'),
                "extraction_id": extraction.id if extraction else None,
                "status": extraction.status if extraction else "Pending",
                "progress": 0.0,
                "progress_details": None
            }

            if extraction:
                prog_data = self.get_extraction_progress(extraction.id)
                total = prog_data['mandatory_total']
                covered = prog_data['mandatory_covered']
                item['progress'] = (covered / total * 100) if total > 0 else 0
                item['progress_details'] = prog_data

            result.append(item)

        return result

    def get_all_papers(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene TODOS los papers del proyecto (vista Owner).
        Flujo:
        1. Pide TODOS los papers del proyecto a ExtractionPhaseService.
        2. Cruza con asignaciones (también del service) y estado local.
        """
        all_studies = self.phase_service.get_all_project_papers(project_id)

        assignments_map = self.phase_service.get_project_assignments_map(project_id)

        study_ids = [s['id'] for s in all_studies]
        local_extractions = {
            ext.study_id: ext
            for ext in PaperExtraction.objects.filter(study_id__in=study_ids)
        }

        result = []
        for study in all_studies:
            study_id = study['id']
            ext = local_extractions.get(study_id)

            assignment_info = assignments_map.get(study_id, {})

            item = {
                "id": study_id,
                "study_id": study_id,
                "title": study['title'],
                "authors": study['authors'],
                "pdf_url": study.get('pdf_url', '#'),

                "extraction_id": ext.id if ext else None,
                "status": ext.status if ext else "Pending",

                "researcher_id": assignment_info.get('researcher_id'),
                "researcher_name": assignment_info.get('researcher_name', 'Sin Asignar'),

                "progress": 0.0
            }

            if ext:
                prog = self.get_extraction_progress(ext.id)
                total = prog['mandatory_total']
                covered = prog['mandatory_covered']
                item['progress'] = (covered / total * 100) if total > 0 else 0

            result.append(item)

        return result

    def _serialize_extraction_with_meta(self, extraction, study_data):
        return {
            "id": extraction.id,
            "study_id": extraction.study_id,
            "status": extraction.status,
            "title": study_data.get('title', 'Unknown'),
            "authors": study_data.get('authors', 'Unknown'),
            "pdf_url": study_data.get('pdf_url')
        }
