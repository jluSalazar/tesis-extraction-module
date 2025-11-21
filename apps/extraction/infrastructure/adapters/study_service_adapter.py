from ...domain.repositories.i_study_repository import IStudyRepository
from django.core.exceptions import ObjectDoesNotExist

# ⚠️ Importación TARDÍA o local para evitar ciclos, o mejor aún,
# importar solo la interfaz pública de la app 'acquisition' si existiera.
# Asumiremos acceso directo al ORM de la otra app por ser monolito,
# pero encapsulado aquí.
try:
    from acquisition.models import Study  # Antes 'papers.Paper'
except ImportError:
    Study = None

class StudyServiceAdapter(IStudyRepository):
    def get_study_details(self, study_id: int) -> dict:
        if not Study:
            return {}
        try:
            study = Study.objects.get(pk=study_id)
            return {
                "id": study.id,
                "title": study.title,
                "authors": study.authors,
                "year": study.year,
                "project_id": study.project_id
            }
        except ObjectDoesNotExist:
            return None

    def exists(self, study_id: int) -> bool:
        if not Study:
            return False
        return Study.objects.filter(pk=study_id).exists()