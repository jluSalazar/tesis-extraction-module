from typing import Optional
from ...domain.repositories.i_acquisition_repository import IAcquisitionRepository

try:
    from apps.acquisition.models import Study  # Ajusta la ruta a tu proyecto real
    from apps.design.models import ResearchQuestion  # Ajusta la ruta
except ImportError:
    Study = None
    ResearchQuestion = None


class AcquisitionServiceAdapter(IAcquisitionRepository):

    def get_study_details(self, study_id: int) -> dict:
        """
        Obtiene detalles del estudio desde la app Acquisition.
        """
        if not Study:
            # Retorno mock o error si la app no existe en el entorno
            return {}

        try:
            study = Study.objects.get(pk=study_id)
            return {
                "id": study.id,
                "title": study.title,
                "year": study.year,
                "project_id": study.project_id  # Asumiendo que Study tiene FK a Project
            }
        except Study.DoesNotExist:
            return None

    def exists(self, study_id: int) -> bool:
        if not Study: return False
        return Study.objects.filter(pk=study_id).exists()

    def get_project_context(self, study_id: int) -> Optional[int]:
        """Helper para obtener el ID del proyecto dado un estudio"""
        details = self.get_study_details(study_id)
        return details.get('project_id')