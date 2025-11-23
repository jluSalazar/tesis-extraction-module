from rest_framework import serializers
from ..domain.value_objects.extraction_status import ExtractionStatus


class QuoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    location = serializers.CharField(required=False, allow_blank=True)
    researcher_id = serializers.IntegerField(read_only=True)

    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

class ExtractionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    study_id = serializers.IntegerField()
    assigned_to_user_id = serializers.IntegerField(read_only=True)
    status = serializers.ChoiceField(choices=[s.value for s in ExtractionStatus])
    started_at = serializers.DateTimeField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)
    quotes = QuoteSerializer(many=True, read_only=True)

    is_active = serializers.BooleanField(read_only=True)

# --- READ SERIALIZERS (Salida) ---

class TagResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    is_mandatory = serializers.BooleanField()
    status = serializers.CharField()
    visibility = serializers.CharField()
    type = serializers.CharField()

class QuoteResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    location = serializers.CharField()
    researcher_id = serializers.IntegerField()
    tags = TagResponseSerializer(many=True)

# --- WRITE SERIALIZERS (Entrada) ---

class CreateQuoteInputSerializer(serializers.Serializer):
    extraction_id = serializers.IntegerField()
    text = serializers.CharField(min_length=1)
    location = serializers.CharField(required=False, allow_blank=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="Lista de IDs de tags a asociar"
    )

class CreateTagInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    project_id = serializers.IntegerField(help_text="ID del proyecto externo")
    is_inductive = serializers.BooleanField(default=True)

class ModerateTagInputSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['APPROVE', 'REJECT'])

class MergeTagInputSerializer(serializers.Serializer):
    target_tag_id = serializers.IntegerField()
    source_tag_id = serializers.IntegerField()