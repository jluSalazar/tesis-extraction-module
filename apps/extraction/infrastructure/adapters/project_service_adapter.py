from typing import List, Optional
from ...domain.repositories.i_project_repository import IProjectRepository
from ...domain.dtos.project_dtos import ProjectDTO, ProjectMemberDTO, StageDTO

# ⚠️ ZONA SUCIA: Importación de modelos de otra app
try:
    from apps.projects.models import Project, Membership, Stage
    from apps.project.service.project_services import ProjectService
except ImportError:
    Project = None
    Membership = None
    Stage = None
    ProjectService = None


class ProjectServiceAdapter(IProjectRepository):
    def __init__(self):
        # Instanciamos el servicio de la otra app
        self.project_service_external = ProjectService() if ProjectService else None

    def get_project_by_id(self, project_id: int) -> Optional[ProjectDTO]:
        if not Project: return None
        try:
            p = Project.objects.get(pk=project_id)
            return ProjectDTO(
                id=p.id,
                name=p.name,
                description=p.description,
                owner_id=p.owner_id
            )
        except Project.DoesNotExist:
            return None

    def exists(self, project_id: int) -> bool:
        if not Project: return False
        return Project.objects.filter(pk=project_id).exists()

    def is_member(self, project_id: int, user_id: int) -> bool:
        if not Membership: return False
        # Verificamos si existe una membresía para ese user y proyecto
        #return Membership.objects.filter(project_id=project_id, user_id=user_id).exists()

        if not Project: return False
        project = Project.objects.get(pk=project_id)
        members = self.project_service_external.get_members(project)
        return members.filter(user_id=user_id).exists()

    def get_members(self, project_id: int) -> List[ProjectMemberDTO]:
        if not Membership: return []

        # Obtenemos todos los miembros
        members = Membership.objects.filter(project_id=project_id)
        return [
            ProjectMemberDTO(
                user_id=m.user_id,
                role=m.role,
                joined_at=m.joined_at
            )
            for m in members
        ]

    def get_current_stage(self, project_id: int) -> Optional[StageDTO]:
        if not Stage: return None

        # Asumimos que queremos la etapa que está "OPENED"
        # O la última etapa modificada. Ajustar lógica según negocio.
        try:
            stage = Stage.objects.filter(
                project_id=project_id,
                status='OPENED'
            ).first()

            if not stage:
                return None

            return StageDTO(
                name=stage.name,
                status=stage.status
            )
        except Exception:
            return None