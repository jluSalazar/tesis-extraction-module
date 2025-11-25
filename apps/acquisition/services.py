from typing import Optional, Dict


class AcquisitionService:
    """
    Servicio público de la app Acquisition.
    MOCK MODE: Retorna datos falsos para desarrollo.
    """

    @staticmethod
    def get_study_details(study_id: int) -> Optional[Dict]:
        """API pública para obtener detalles de un estudio (MOCK)"""
        if study_id == 999:
            return None

        return {
            "id": study_id,
            "title": f"Estudio Simulado #{study_id}: Impacto de la IA en Legacy Code",
            "year": 2024,
            "project_id": 1,
            "authors": "Dr. House, John Doe",
        }

    @staticmethod
    def exists(study_id: int) -> bool:
        """Verifica existencia del estudio (MOCK)"""
        return study_id != 999

    @staticmethod
    def get_project_id(study_id: int) -> Optional[int]:
        """Obtiene el ID del proyecto al que pertenece el estudio (MOCK)"""
        if study_id == 999:
            return None
        return 1