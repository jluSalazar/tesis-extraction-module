from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import TagService

class TagConfigurationStatusView(APIView):
    """
    Endpoint para que el Owner verifique si la configuración es válida
    y para que el sistema decida si mostrar la lista a los Researchers.
    """
    def get(self, request, project_id):
        service = TagService()
        status_data = service.get_tag_configuration_status(project_id)
        return Response(status_data)

class MandatoryTagsView(APIView):
    """
    Endpoint para listar los tags que el researcher DEBE llenar.
    """
    def get(self, request, project_id):
        service = TagService()
        tags = service.get_mandatory_tags(project_id)
        return Response(tags)