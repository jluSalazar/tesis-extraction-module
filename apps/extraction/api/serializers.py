from rest_framework import serializers
from ..domain.value_objects.extraction_status import ExtractionStatus


# --- WRITE SERIALIZERS (Entrada) ---

class CreateQuoteInputSerializer(serializers.Serializer):
    extraction_id = serializers.IntegerField()
    text = serializers.CharField(min_length=1, max_length=5000)
    location = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200
    )
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="Lista de IDs de tags a asociar"
    )


class CreateTagInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, min_length=1)
    project_id = serializers.IntegerField(help_text="ID del proyecto externo")
    is_inductive = serializers.BooleanField(default=True)
    question_id = serializers.IntegerField(required=False, allow_null=True)


class ModerateTagInputSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['APPROVE', 'REJECT'])


class MergeTagInputSerializer(serializers.Serializer):
    target_tag_id = serializers.IntegerField()
    source_tag_id = serializers.IntegerField()


# --- READ SERIALIZERS (Salida) ---

class TagResponseSerializer(serializers.Serializer):
    """Serializer para respuestas de Tag"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    project_id = serializers.IntegerField()
    is_mandatory = serializers.BooleanField()
    status = serializers.CharField()
    visibility = serializers.CharField()
    type = serializers.CharField()
    created_by_user_id = serializers.IntegerField()
    question_id = serializers.IntegerField(allow_null=True)


class QuoteResponseSerializer(serializers.Serializer):
    """Serializer para respuestas de Quote"""
    id = serializers.IntegerField()
    text = serializers.CharField()
    location = serializers.CharField()
    researcher_id = serializers.IntegerField()
    tags = TagResponseSerializer(many=True)


class ExtractionListSerializer(serializers.Serializer):
    """Serializer ligero para listados"""
    id = serializers.IntegerField()
    study_id = serializers.IntegerField()
    status = serializers.CharField()
    started_at = serializers.DateTimeField(allow_null=True)
    completed_at = serializers.DateTimeField(allow_null=True)
    quotes_count = serializers.IntegerField()  # Agregado


class ExtractionDetailSerializer(serializers.Serializer):
    """Serializer completo para detalles"""
    id = serializers.IntegerField()
    study_id = serializers.IntegerField()
    assigned_to_user_id = serializers.IntegerField(allow_null=True)
    status = serializers.CharField()
    started_at = serializers.DateTimeField(allow_null=True)
    completed_at = serializers.DateTimeField(allow_null=True)
    quotes = QuoteResponseSerializer(many=True)
    is_active = serializers.BooleanField()


class CreateExtractionInputSerializer(serializers.Serializer):
    """Input para crear extracción"""
    study_id = serializers.IntegerField()