from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema  # Opcional, para doc

from ..container import container
from ..application.commands.create_extraction import CreateExtractionCommand
from ..application.commands.complete_extraction import CompleteExtractionCommand
from ..application.commands.create_quote import CreateQuoteCommand
from ..application.commands.create_tag import CreateTagCommand
from ..application.commands.moderate_tag import ModerateTagCommand
from ..application.commands.merge_tags import MergeTagsCommand
from ..application.queries.get_extraction import GetExtractionQuery
from ..application.queries.list_extractions import ListExtractionsQuery

from . import serializers as dtos  # Alias para diferenciar
from ..domain.exceptions.extraction_exceptions import ExtractionValidationError


class ExtractionViewSet(viewsets.ViewSet):
    """Maneja el Aggregate Root: Extraction"""

    def list(self, request):
        query = ListExtractionsQuery(user_id=request.user.id)
        extractions = container.list_extractions_handler.handle(query)
        # Nota: Aquí deberíamos tener un serializer de salida para la lista
        data = [{"id": e.id, "status": e.status, "study_id": e.study_id} for e in extractions]
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        query = GetExtractionQuery(extraction_id=int(pk))
        try:
            extraction = container.get_extraction_handler.handle(query)
            # Mapeo manual a respuesta o usar un Serializer de Salida
            # Por simplicidad, retornamos dict, pero idealmente usar ExtractionSerializer
            return Response({
                "id": extraction.id,
                "study_id": extraction.study_id,
                "status": extraction.status,
                "quotes": len(extraction.quotes)  # Ejemplo
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ExtractionValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def create(self, request):
        serializer = dtos.ExtractionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = CreateExtractionCommand(
            study_id=serializer.validated_data['study_id'],
            user_id=request.user.id
        )

        try:
            extraction = container.create_extraction_handler.handle(command)
            return Response({"id": extraction.id, "status": extraction.status}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ExtractionValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        command = CompleteExtractionCommand(
            extraction_id=int(pk),
            user_id=request.user.id
        )
        try:
            container.complete_extraction_handler.handle(command)
            return Response({"status": "Completed"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ExtractionValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class QuoteViewSet(viewsets.ViewSet):
    """Maneja la entidad secundaria: Quote"""

    def create(self, request):
        serializer = dtos.CreateQuoteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        command = CreateQuoteCommand(
            extraction_id=data['extraction_id'],
            text=data['text'],
            location=data.get('location', ''),
            user_id=request.user.id,
            tag_ids=data['tag_ids']
        )

        try:
            quote = container.create_quote_handler.handle(command)
            return Response({"id": quote.id, "text": quote.text}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ExtractionValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TagViewSet(viewsets.ViewSet):
    """Maneja la entidad: Tag (Propuesta y Moderación)"""

    def create(self, request):
        serializer = dtos.CreateTagInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        command = CreateTagCommand(
            name=data['name'],
            user_id=request.user.id,
            project_id=data['project_id'],
            is_inductive=data['is_inductive']
        )

        try:
            tag = container.create_tag_handler.handle(command)
            return Response({"id": tag.id, "status": tag.status}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ExtractionValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(detail=True, methods=['post'])
    def moderate(self, request, pk=None):
        """Aprobar o Rechazar Tag"""
        serializer = dtos.ModerateTagInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = ModerateTagCommand(
            tag_id=int(pk),
            action=serializer.validated_data['action'],
            owner_id=request.user.id
        )

        try:
            container.moderate_tag_handler.handle(command)
            return Response({"status": "Moderated"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ExtractionValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(detail=False, methods=['post'], url_path='merge')
    def merge(self, request):
        """Fusionar tags"""
        serializer = dtos.MergeTagInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = MergeTagsCommand(
            target_tag_id=serializer.validated_data['target_tag_id'],
            source_tag_id=serializer.validated_data['source_tag_id']
        )

        try:
            container.merge_tags_handler.handle(command)
            return Response({"status": "Merged"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ExtractionValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)