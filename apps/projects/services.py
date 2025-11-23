from typing import List, Optional, Dict
from datetime import datetime


# from .models import Project, Membership, Stage <-- COMENTADO TEMPORALMENTE

class ProjectService:
    """
    Servicio público de la app Projects.
    MOCK MODE: Retorna datos falsos para desarrollo.
    """

    @staticmethod
    def get_project_details(project_id: int) -> Optional[Dict]:
        if project_id == 999:
            return None

        return {
            "id": project_id,
            "name": "Proyecto SLR: Modernización de Sistemas",
            "description": "Revisión sistemática sobre patrones de modernización.",
            "owner_id": 1,  # Asumimos user ID 1 como owner
        }

    @staticmethod
    def exists(project_id: int) -> bool:
        return project_id != 999

    @staticmethod
    def is_member(project_id: int, user_id: int) -> bool:
        # Simulación: Siempre retorna True para facilitar pruebas de desarrollo
        # excepto si el user_id es -1
        return user_id != -1

    @staticmethod
    def get_members(project_id: int) -> List[Dict]:
        return [
            {
                "user_id": 1,
                "role": "OWNER",
                "joined_at": datetime.now(),
            },
            {
                "user_id": 2,
                "role": "COLLABORATOR",
                "joined_at": datetime.now(),
            }
        ]

    @staticmethod
    def get_current_stage(project_id: int) -> Optional[Dict]:
        # Simula que el proyecto está en etapa de Extracción
        return {
            "name": "EXTRACTION",
            "status": "OPENED",
        }