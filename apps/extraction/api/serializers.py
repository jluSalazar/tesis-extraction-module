from rest_framework import serializers
from ..domain.value_objects.extraction_status import ExtractionStatus

class QuoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    location = serializers.CharField(required=False, allow_blank=True)
    researcher_id = serializers.IntegerField(read_only=True)
    # Tags podrían ser una lista de IDs para simplificar la entrada
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

    # Campos calculados o enriquecidos (opcional)
    is_active = serializers.BooleanField(read_only=True)