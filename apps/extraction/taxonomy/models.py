from django.db import models
from django.utils.translation import gettext_lazy as _

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
    
    created_by_id = models.IntegerField(null=True, db_index=True)
    
    question_id = models.IntegerField(
        null=True, 
        blank=True, 
        db_index=True,
        help_text="ID de la ResearchQuestion externa"
    )
    
    project_id = models.IntegerField(db_index=True)

    type = models.CharField(
        max_length=20, 
        choices=TagType.choices, 
        default=TagType.DEDUCTIVE
    )
    approval_status = models.CharField(
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.APPROVED  # Los deductivos se aprueban automáticamente
    )
    merged_into = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='merged_from'
    )
    is_mandatory = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Constraints lógicos en lugar de FKs
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'project_id', 'question_id'],
                name='unique_tag_per_context'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"