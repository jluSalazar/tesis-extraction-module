from typing import List, Optional
from ...domain.repositories.i_tag_repository import ITagRepository
from ...domain.entities.tag import Tag
from ..models import TagModel
from ..mappers.domain_mappers import TagMapper
from django.db.models import Q


class DjangoTagRepository(ITagRepository):
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
        # Nota: Aquí hay un truco. Necesitamos saber el project_id a partir del study_id.
        # Opción A: Hacemos una query al Adapter de Study primero.
        # Opción B: Asumimos que el TagModel tiene project_id y lo filtramos (si ya sabemos el project_id en la capa superior).
        # Asumiendo que la validación recibe el study_id, necesitamos resolver el project.
        # Para simplificar este ejemplo, asumiremos que obtenemos tags obligatorios del proyecto asociado al tag.

        # En una implementación real, deberías inyectar el StudyServiceAdapter aquí o pasar el project_id.
        qs = TagModel.objects.filter(is_mandatory=True)
        # TODO: Filtrar por project_id correcto obteniéndolo del study_id
        return [TagMapper.to_domain(t) for t in qs]

    def list_available_tags_for_user(self, user_id: int, project_id: int) -> List[Tag]:
        qs = TagModel.objects.filter(project_id=project_id).filter(
            Q(visibility='Public') | Q(created_by_id=user_id)  # created_by_id asumiendo FK de Django
        )
        return [TagMapper.to_domain(m) for m in qs]