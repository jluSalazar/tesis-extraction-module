from typing import List, Optional
from ...domain.repositories.i_tag_repository import ITagRepository
from ...domain.entities.tag import Tag
from ..models import TagModel
from ..mappers.domain_mappers import TagMapper
from django.db.models import Q


class DjangoTagRepository(ITagRepository):
    def __init__(self, acquisition_adapter):
        self.acquisition_adapter = acquisition_adapter

    def get_by_ids(self, tag_ids: List[int]) -> List[Tag]:
        qs = TagModel.objects.filter(pk__in=tag_ids)
        return [TagMapper.to_domain(m) for m in qs]

    def get_by_id(self, tag_id: int) -> Tag:
        model = TagModel.objects.get(pk=tag_id)
        return TagMapper.to_domain(model)

    def save(self, tag: Tag) -> Tag:
        # Mapeo inverso manual o simple
        data = {
            'name': tag.name,
            'is_mandatory': tag.is_mandatory,
            'created_by_user_id': tag.created_by_user_id,  # Asegúrate que tu modelo tenga este campo o 'created_by_id'
            'status': tag.status.value,
            'visibility': tag.visibility.value,
            'type': tag.type.value
            # project_id y question_id deberían venir en la entidad o manejarse aquí
        }

        obj, created = TagModel.objects.update_or_create(pk=tag.id, defaults=data)
        return TagMapper.to_domain(obj)

    def delete(self, tag: Tag) -> None:
        TagModel.objects.filter(pk=tag.id).delete()

    def get_mandatory_tags_for_project_context(self, study_id: int) -> List[Tag]:
        # Opción 1: Join si Study está en la misma DB (Monolito) y tienes FK
        # Opción 2 (Mejor para desacoplar): Pasar project_id explícitamente desde el Handler
        # Opción 3 (Tu caso): Obtener project_id vía adapter

        # Asumiendo que TagModel tiene project_id
        project_id = self.acquisition_adapter.get_project_context(study_id)
        qs = TagModel.objects.filter(project_id=project_id, is_mandatory=True)
        return [TagMapper.to_domain(t) for t in qs]

    def list_available_tags_for_user(self, user_id: int, project_id: int) -> List[Tag]:
        qs = TagModel.objects.filter(project_id=project_id).filter(
            Q(visibility='Public') | Q(created_by_id=user_id)  # created_by_id asumiendo FK de Django
        )
        return [TagMapper.to_domain(m) for m in qs]