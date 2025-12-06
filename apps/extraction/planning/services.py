
from ..taxonomy.models import Tag, VisibilityChoices
from ..planning.models import ExtractionPhase
from ..external.interfaces import IProjectService



class ExtractionPhaseService:
    """
    Servicio de Dominio para manejar la Fase de Extracción.
    """

    def __init__(self, project_service: IProjectService = None):
        # En un entorno real, usarías un mecanismo de inyección de dependencias.
        # Aquí, asumimos que se recibe la interfaz IProjectService.
        self._project_service = project_service

    def get_tag_list_visibility(self, project_id: int) -> bool:
        """
        Determina si la lista de tags para el proyecto debe ser visible (PUBLIC).
        La visibilidad está definida en la fase de extracción.
        """
        try:
            # En un entorno real, aquí se buscaría la fase de extracción
            # phase = ExtractionPhase.objects.get(project_id=project_id)

            # --- MOCK: Simular obtención del estado de visibilidad del Tag ---
            # Para el escenario, la visibilidad la determina el Tag.
            # Buscamos un tag para determinar si la fase es pública o privada.
            # Usaremos la lógica simple: si hay AL MENOS un tag público, la lista es pública.

            # Buscamos si existe al menos un tag con visibilidad PUBLIC.
            # En la vida real, este campo debería estar en ExtractionPhase.
            has_public_tag = Tag.objects.filter(
                extraction_phase__project_id=project_id,
                visibility=VisibilityChoices.PUBLIC
            ).exists()

            return has_public_tag

        except ExtractionPhase.DoesNotExist:
            # Si no existe la fase, la visibilidad es falsa.
            return False
        # Manejo de otros errores...
