from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..container import container
from ..application.commands.create_extraction import CreateExtractionCommand
from ..application.commands.complete_extraction import CompleteExtractionCommand
from ..domain.exceptions.extraction_exceptions import ExtractionValidationError
from .serializers import ExtractionSerializer  # Asumimos que existe


class ExtractionViewSet(viewsets.ViewSet):
    """
    ViewSet que delega la lógica a la Capa de Aplicación.
    """

    def create(self, request):
        serializer = ExtractionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = CreateExtractionCommand(
            study_id=serializer.validated_data['study_id'],
            user_id=request.user.id
        )

        try:
            extraction = container.create_extraction_handler.handle(command)
            # Convertimos entidad de vuelta a dict/serializer para la respuesta
            return Response({"id": extraction.id, "status": extraction.status}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        command = CompleteExtractionCommand(
            extraction_id=pk,
            user_id=request.user.id
        )

        try:
            container.complete_extraction_handler.handle(command)
            return Response({"status": "Completed"}, status=status.HTTP_200_OK)
        except ExtractionValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)