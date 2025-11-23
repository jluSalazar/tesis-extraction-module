from django.db import models
from django.conf import settings
from django.utils import timezone
from ..domain.value_objects.extraction_status import ExtractionStatus
from ..domain.value_objects.tag_status import TagStatus
from ..domain.value_objects.tag_type import TagType
from ..domain.value_objects.tag_visibility import TagVisibility


class ExtractionModel(models.Model):
    """Modelo de persistencia para la entidad Extraction."""
    study_id = models.BigIntegerField(
        help_text="ID del estudio en el servicio de Acquisition/Studies",
        db_index=True
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='extractions'
    )
    status = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.value) for tag in ExtractionStatus],
        default=ExtractionStatus.PENDING
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'extraction_extraction'
        indexes = [
            models.Index(fields=['study_id', 'assigned_to']),
        ]

class TagModel(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default="#FFFFFF")
    type = models.CharField(
        max_length=20,
        choices=[(t.value, t.value) for t in TagType],
        default=TagType.DEDUCTIVE
    )
    is_mandatory = models.BooleanField(default=False)
    question_id = models.IntegerField(null=True, blank=True)
    project_id = models.IntegerField(help_text="Project context ID")
    created_by_user_id = models.IntegerField(help_text="User ID")
    status = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in TagStatus],
        default=TagStatus.PENDING.value
    )
    visibility = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in TagVisibility],
        default=TagVisibility.PRIVATE.value
    )

    class Meta:
        db_table = 'extraction_tag'

class QuoteModel(models.Model):
    extraction = models.ForeignKey(
        ExtractionModel,
        on_delete=models.CASCADE,
        related_name='quotes'
    )
    text_portion = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    researcher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    tags = models.ManyToManyField(TagModel, related_name='quotes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'extraction_quote'