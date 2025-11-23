from dataclasses import dataclass

from django.db import transaction

from apps.extraction.domain.repositories.i_tag_repository import ITagRepository


@dataclass
class ModerateTagCommand:
    tag_id: int
    action: str  # 'APPROVE' or 'REJECT'
    owner_id: int  # Para validar que quien modera tiene permisos


class ModerateTagHandler:
    def __init__(self, tag_repo: ITagRepository):
        self.tag_repo = tag_repo

    @transaction.atomic
    def handle(self, command):
        tag = self.tag_repo.get_by_id(command.tag_id)

        if command.action == 'APPROVE':
            tag.approve()
        elif command.action == 'REJECT':
            tag.reject()

        self.tag_repo.save(tag)