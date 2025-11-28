from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.extraction.planning.models import ExtractionPhase

class Tag(models.Model):
    """
    Entidad Tag.
    No tiene FK a ResearchQuestion, solo guarda el ID de referencia.
    """
    class TagType(models.TextChoices):
        DEDUCTIVE = 'deductive', _('Deductivo')
        INDUCTIVE = 'inductive', _('Inductivo')

    class ApprovalStatus(models.TextChoices):
        PENDING = 'pending', _('Pendiente de Aprobación')
        APPROVED = 'approved', _('Aprobado')
        REJECTED = 'rejected', _('Rechazado')

    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, default='#FFFFFF')
    justification = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tags',
        db_index=True
    )

    question_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        help_text="ID de la ResearchQuestion (App Design)"
    )

    extraction_phase = models.ForeignKey(
        ExtractionPhase,
        on_delete=models.CASCADE,
        related_name='tags'
    )

    type = models.CharField(
        max_length=20, 
        choices=TagType.choices, 
        default=TagType.DEDUCTIVE
    )
    
    approval_status = models.CharField(
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.APPROVED
    )
    
    is_mandatory = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    merged_into = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='merged_from'
    )

    class Meta:
        indexes = [
            models.Index(fields=['extraction_phase', 'approval_status']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['extraction_phase', 'name'],
                name='unique_tag_name_per_phase'
            )
        ]
        verbose_name = _("Etiqueta")
        verbose_name_plural = _("Etiquetas")

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    @property
    def is_active(self) -> bool:
        return self.merged_into is None
