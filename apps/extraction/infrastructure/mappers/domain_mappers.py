from typing import List
from ...domain.entities.extraction import Extraction
from ...domain.entities.quote import Quote
from ...domain.entities.tag import Tag
from ...domain.value_objects.extraction_status import ExtractionStatus
from ..models import ExtractionModel, QuoteModel, TagModel
from ...domain.value_objects.tag_status import TagStatus
from ...domain.value_objects.tag_type import TagType
from ...domain.value_objects.tag_visibility import TagVisibility


class ExtractionMapper:
    @staticmethod
    def to_domain(model: ExtractionModel) -> Extraction:
        if not model:
            return None

        # Mapeo recursivo de quotes (Optimización: usar prefetch_related en el repo)
        quotes_domain = [QuoteMapper.to_domain(q) for q in model.quotes.all()]

        return Extraction(
            id=model.id,
            study_id=model.study_id,
            assigned_to_user_id=model.assigned_to_id if model.assigned_to else None,
            status=ExtractionStatus(model.status),
            started_at=model.started_at,
            completed_at=model.completed_at,
            quotes=quotes_domain
        )

    @staticmethod
    def to_db(entity: Extraction) -> dict:
        """Retorna diccionario para crear/actualizar modelo Django"""
        return {
            'study_id': entity.study_id,
            'assigned_to_id': entity.assigned_to_user_id,
            'status': entity.status.value,
            'started_at': entity.started_at,
            'completed_at': entity.completed_at
        }


class QuoteMapper:
    @staticmethod
    def to_domain(model: QuoteModel) -> Quote:
        tags_domain = [TagMapper.to_domain(t) for t in model.tags.all()]
        return Quote(
            id=model.id,
            text=model.text_portion,
            location=model.location,
            researcher_id=model.researcher_id,
            tags=tags_domain
        )


class TagMapper:
    @staticmethod
    def to_domain(model: TagModel) -> Tag:
        # Lógica de mapeo simple
        return Tag(
            id=model.id,
            name=model.name,
            project_id=model.project_id,
            is_mandatory=model.is_mandatory,
            created_by_user_id=model.created_by_user_id,
            question_id=model.question_id,
            status=TagStatus(model.status),
            visibility=TagVisibility(model.visibility),
            type=TagType(model.type),
        )

    @staticmethod
    def to_db(entity: Tag) -> TagModel:
        return TagModel(
            id=entity.id,
            name=entity.name,
            project_id=entity.project_id,
            is_mandatory=entity.is_mandatory,
            created_by_user_id=entity.created_by_user_id,
            question_id=entity.question_id,
            status=entity.status.value,
            visibility=entity.visibility.value,
            type=entity.type.value,
        )
