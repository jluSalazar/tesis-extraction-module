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

    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, default='#FFFFFF')
    justification = models.TextField(blank=True)
    
    # Referencia débil a Identity Management (Users)
    created_by_id = models.IntegerField(null=True, db_index=True)
    
    # Referencia débil al Bounded Context 'Design'
    question_id = models.IntegerField(
        null=True, 
        blank=True, 
        db_index=True,
        help_text="ID de la ResearchQuestion externa"
    )
    
    # Contexto del proyecto (Multi-tenancy lógico)
    project_id = models.IntegerField(db_index=True)

    type = models.CharField(
        max_length=20, 
        choices=TagType.choices, 
        default=TagType.DEDUCTIVE
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