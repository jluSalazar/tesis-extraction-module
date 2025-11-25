from typing import List, Optional, Dict
from datetime import datetime


class DesignService:
    """
    Servicio público de la app Design.
    MOCK MODE: Retorna datos falsos para desarrollo.
    """

    @staticmethod
    def get_question_details(question_id: int) -> Optional[Dict]:
        if question_id == 999:
            return None

        return {
            "id": question_id,
            "text": "¿Cómo afecta el TDD a la productividad en equipos pequeños?",
            "project_id": 1,
            "created_at": datetime.now(),
        }

    @staticmethod
    def get_questions_by_project(project_id: int) -> List[Dict]:
        """Retorna 2 preguntas dummy siempre"""
        return [
            {
                "id": 101,
                "text": "¿Cuáles son los principales retos de la migración a microservicios?",
                "project_id": project_id,
            },
            {
                "id": 102,
                "text": "¿Qué métricas definen el éxito en Clean Architecture?",
                "project_id": project_id,
            }
        ]

    @staticmethod
    def question_exists(question_id: int) -> bool:
        return question_id != 999