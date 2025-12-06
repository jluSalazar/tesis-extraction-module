from typing import List, Optional, Dict
from django.db import transaction

# Modelos y Opciones de Extracción
from .models import  Tag, TagTypeChoices, VisibilityChoices
from ..planning.models import ExtractionPhase
from ..external.interfaces import IDesignService, IProjectService
from ..core.models import PaperExtraction
# Interfaz y DTOs de apps externas
from ..external.dtos import ProjectStageDTO

class TagService:
    """
    Servicio de Dominio para manejar la creación y gestión de Tags.
    """

    def __init__(self, design_service: IDesignService = None):
        self._design_service = design_service

    @transaction.atomic
    def create_tag(
            self,
            project_id: int,
            name: str,
            question_id: Optional[int],
            user_id: int
    ) -> Tag:
        """
        Crea un nuevo Tag Deductivo y determina su estado obligatorio y visibilidad.
        """
        # 1. Obtener/Crear Phase: Necesitamos la fase para enlazar el tag.
        # En un proyecto real, se garantiza que la fase existe.
        # MOCK: Creamos/obtenemos la fase para simular el FK.
        phase, _ = ExtractionPhase.objects.get_or_create(
            project_id=project_id,
            defaults={'status': 'OPEN'}  # Simulamos que está abierta
        )

        # 2. Determinar is_mandatory
        is_mandatory = False
        if question_id:
            # La lógica del escenario dice: "es obligatorio si el tag está relacionado a la pregunta sí"
            if self._design_service.question_exists(question_id):
                is_mandatory = True

        # 3. Determinar visibility
        # El escenario 2 establece la visibilidad:
        # Visibilidad: PUBLIC si hay al menos 1 Tag relacionado a PI. PRIVATE si no hay.
        visibility = VisibilityChoices.PRIVATE
        if is_mandatory:
            visibility = VisibilityChoices.PUBLIC

        # 4. Crear el Tag
        tag = Tag.objects.create(
            extraction_phase=phase,
            name=name,
            rq_related_id=question_id,
            is_mandatory=is_mandatory,
            created_by_id=user_id,
            type=TagTypeChoices.DEDUCTIVE,
            visibility=visibility  # Se define aquí, y luego la fase lo usa.
            # status se mantiene como PENDING
        )
        return tag

    def get_mandatory_tag_names(self, project_id: int) -> List[str]:
        """
        Obtiene la lista de nombres de tags marcados como obligatorios para el proyecto.
        """
        # Filtra los tags que pertenecen a la fase del proyecto y que son obligatorios.
        mandatory_tags = Tag.objects.filter(
            extraction_phase__project_id=project_id,
            is_mandatory=True
        ).values_list('name', flat=True)

        return list(mandatory_tags)