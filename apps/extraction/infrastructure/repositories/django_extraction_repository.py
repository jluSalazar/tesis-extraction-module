from typing import Optional, List
from django.db import transaction
from ...domain.repositories.i_extraction_repository import IExtractionRepository
from ...domain.entities.extraction import Extraction
from ..models import ExtractionModel
from ..mappers.domain_mappers import ExtractionMapper


class DjangoExtractionRepository(IExtractionRepository):
    def get_by_id(self, extraction_id: int) -> Optional[Extraction]:
        try:
            # Usamos select_related/prefetch para evitar N+1 al convertir a dominio
            model = ExtractionModel.objects.prefetch_related(
                'quotes__tags'
            ).get(pk=extraction_id)
            return ExtractionMapper.to_domain(model)
        except ExtractionModel.DoesNotExist:
            return None

    def get_by_study_id(self, study_id: int) -> Optional[Extraction]:
        try:
            model = ExtractionModel.objects.prefetch_related(
                'quotes__tags'
            ).get(study_id=study_id)
            return ExtractionMapper.to_domain(model)
        except ExtractionModel.DoesNotExist:
            return None

    @transaction.atomic
    def save(self, extraction: Extraction) -> Extraction:
        data = ExtractionMapper.to_db(extraction)

        if extraction.id:
            ExtractionModel.objects.filter(pk=extraction.id).update(**data)
            model = ExtractionModel.objects.get(pk=extraction.id)
        else:
            model = ExtractionModel.objects.create(**data)
            extraction.id = model.id

        # Nota: La persistencia de Quotes hijos suele manejarse en repositorios de Quotes
        # o aquí si es una actualización profunda del agregado.
        # Por simplicidad (KISS), asumimos que las quotes se guardan individualmente
        # o implementamos lógica extra aquí.

        return ExtractionMapper.to_domain(model)

    def list_by_user(self, user_id: int) -> List[Extraction]:
        qs = ExtractionModel.objects.filter(assigned_to_id=user_id)
        return [ExtractionMapper.to_domain(m) for m in qs]