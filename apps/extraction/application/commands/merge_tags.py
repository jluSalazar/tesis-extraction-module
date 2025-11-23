from dataclasses import dataclass

from django.db import transaction


@dataclass
class MergeTagsCommand:
    target_tag_id: int  # El que queda (ej: "Costo oculto")
    source_tag_id: int  # El que desaparece (ej: "Costos oc.")


class MergeTagsHandler:
    def __init__(self, tag_repo, quote_repo, merge_service):
        self.tag_repo = tag_repo
        self.merge_service = merge_service

    @transaction.atomic
    def handle(self, command):
        target = self.tag_repo.get_by_id(command.target_tag_id)
        source = self.tag_repo.get_by_id(command.source_tag_id)

        # Usamos el servicio de dominio para la lógica compleja
        self.merge_service.merge_tags(target, source)