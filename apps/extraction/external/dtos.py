from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectMemberDTO:
    """Contrato de datos para un miembro del proyecto (sin modelo Django asociado)."""
    project_id: int
    user_id: int
    role: str
    joined_at: datetime

@dataclass(frozen=True)
class ProjectStageDTO:
    """Contrato de datos para la etapa actual del proyecto (sin modelo Django asociado)."""
    id: int
    name: str
    status: str