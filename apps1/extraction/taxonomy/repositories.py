from typing import List
from .models import Tag


class TagRepository:
    """
    Abstracción para el acceso a datos de Tags.
    Principio DIP (Dependency Inversion): Los servicios dependen de esta clase, no del ORM directamente.
    """

    @staticmethod
    def get_mandatory_for_project(project_id: int) -> List[Tag]:
        return list(Tag.objects.filter(
            question__project_id=project_id,
            is_mandatory=True
        ))

    @staticmethod
    def get_project_taxonomy(project_id: int, public_only: bool = True):
        qs = Tag.objects.filter(question__project_id=project_id)
        if public_only:
            qs = qs.filter(is_public=True)
        return qs