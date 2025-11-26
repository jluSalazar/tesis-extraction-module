from typing import List, Optional, Dict
from datetime import datetime


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
            "owner_id": 1,
        }

    @staticmethod
    def exists(project_id: int) -> bool:
        return project_id != 999

    @staticmethod
    def is_member(project_id: int, user_id: int) -> bool:
        return user_id != -1

    @staticmethod
    def get_members(project_id: int) -> List[Dict]:
        return [
            {"user_id": 1, "role": "OWNER", "joined_at": datetime.now()},
            {"user_id": 2, "role": "COLLABORATOR", "joined_at": datetime.now()},
        ]

    @staticmethod
    def get_current_stage(project_id: int) -> Optional[Dict]:
        return {
            "name": "EXTRACTION",
            "status": "OPENED",
        }
