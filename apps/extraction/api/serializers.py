from rest_framework import serializers
from ..domain.value_objects.extraction_status import ExtractionStatus
from ..domain.value_objects.tag_status import TagStatus
from ..domain.value_objects.tag_visibility import TagVisibility

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