from typing import List, Optional
from .models import Tag


class TagRepository:
    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        try:
            return Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return None

    def list_by_project(self, project_id: int) -> List[Tag]:
        return list(Tag.objects.filter(project_id=project_id))

    def get_mandatory_tags(self, project_id: int) -> List[Tag]:
        return list(Tag.objects.filter(project_id=project_id, is_mandatory=True))

    def create(self, **kwargs) -> Tag:
        return Tag.objects.create(**kwargs)

    def update(self, tag: Tag, **kwargs) -> Tag:
        for key, value in kwargs.items():
            setattr(tag, key, value)
        tag.save()
        return tag

    def delete(self, tag: Tag):
        tag.delete()