from dataclasses import dataclass
from typing import Optional

from ...domain.entities.tag import Tag
from ...domain.repositories.i_design_repository import IDesignRepository
from ...domain.value_objects.tag_type import TagType
from ...domain.value_objects.tag_status import TagStatus
from ...domain.value_objects.tag_visibility import TagVisibility
from ...domain.repositories.i_tag_repository import ITagRepository

@dataclass
class CreateTagCommand:
    name: str
    user_id: int
    project_id: int # Necesario para el contexto
    is_inductive: bool
    question_id: Optional[int] = None

class CreateTagHandler:
    def __init__(self, tag_repo: ITagRepository, design_repo: IDesignRepository):
        self.tag_repo = tag_repo
        self.design_repo = design_repo

    def handle(self, command: CreateTagCommand):
        if command.question_id:
            if not self.design_repo.question_exists(command.question_id):
                raise ValueError(f"La pregunta de investigación {command.question_id} no existe.")

            # Opcional: Obtener detalles para verificar que pertenece al mismo proyecto
            question_dto = self.design_repo.get_question_by_id(command.question_id)
            if question_dto.project_id != command.project_id:
                raise ValueError("La pregunta no pertenece al proyecto indicado.")

        status = TagStatus.PENDING if command.is_inductive else TagStatus.APPROVED
        visibility = TagVisibility.PRIVATE if command.is_inductive else TagVisibility.PUBLIC
        type_ = TagType.INDUCTIVE if command.is_inductive else TagType.DEDUCTIVE

        tag = Tag(
            id=None, # Se genera en DB
            name=command.name,
            is_mandatory=False, # Inductivos no son obligatorios al nacer
            created_by_user_id=command.user_id,
            status=status,
            visibility=visibility,
            type=type_
            # project_id debe manejarse en la persistencia o entidad
        )
        return self.tag_repo.save(tag)