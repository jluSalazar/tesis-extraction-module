from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.extraction.shared.exceptions import BusinessRuleViolation, ResourceNotFound
from .services import ExtractionService

class ExtractionProgressView(APIView):
    """
    Muestra al investigador qué tags le faltan y el estado actual.
    Cumple con: "Entonces el estado del paper debe ser... Y se debe notificar... tags pendientes"
    """
    def get(self, request, extraction_id):
        service = ExtractionService()
        try:
            data = service.get_extraction_progress(extraction_id)
            return Response(data)
        except ResourceNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CompleteExtractionView(APIView):
    """
    Acción de finalizar la extracción.
    """
    def post(self, request, extraction_id):
        service = ExtractionService()
        try:
            # Asumimos que request.user.id está disponible
            extraction = service.complete_extraction(extraction_id, request.user.id)
            return Response({
                "id": extraction.id,
                "status": extraction.status,
                "message": "Extracción completada exitosamente."
            })
        except BusinessRuleViolation as e:
            # Retornamos 400 Bad Request con el mensaje de los tags faltantes
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ResourceNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)