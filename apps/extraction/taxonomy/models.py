from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


from ..external.models import ResearchQuestion
from ..shared.audit import AuditModel
from ..planning.models import ExtractionPhase


User = get_user_model()


class TagTypeChoices:
    """Opciones para el tipo de Tag."""
    DEDUCTIVE = 'DEDUCTIVE'
    INDUCTIVE = 'INDUCTIVE'

    CHOICES = [
        (DEDUCTIVE, 'Deductiva'),
        (INDUCTIVE, 'Inductiva'),
    ]

class ApprovalStatusChoices:
    """Opciones para el estado de aprobación/revisión (usado en Tag y posiblemente otros)."""
    PENDING = 'PENDING'
    APROVED = 'APROVED'
    REJECTED = 'REJECTED'

    CHOICES = [
        (PENDING, 'Pendiente'),
        (APROVED, 'Aprobada'),
        (REJECTED, 'Rechazada'),
    ]


class VisibilityChoices:
    """Opciones para la visibilidad (usado en Tag)."""
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'

    CHOICES = [
        (PUBLIC, 'Pública'),
        (PRIVATE, 'Privada'),
    ]


class Tag(AuditModel):
    """Etiquetas que se pueden agregar a una extracción de texto (Quote)."""

    hex_validator = RegexValidator(
        regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        message="El color debe ser un código hexadecimal válido (e.g., #FF00AA)."
    )

    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Etiqueta")
    color = models.CharField(
        max_length=7,
        validators=[hex_validator],
        verbose_name="Color Hexadecimal"
    )
    extraction_phase = models.ForeignKey(
        ExtractionPhase,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name="Fase de Extracción"
    )
    rq_related = models.ForeignKey(
        ResearchQuestion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tags',
        verbose_name="Pregunta de Investigación Relacionada"
    )
    is_mandatory = models.BooleanField(
        default=False,
        verbose_name="Es Obligatoria"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tags',
        verbose_name="Creado Por"
    )
    type = models.CharField(
        max_length=10,
        choices=TagTypeChoices.CHOICES,
        default=TagTypeChoices.DEDUCTIVE,
        verbose_name="Tipo de Etiqueta"
    )
    status = models.CharField(
        max_length=10,
        choices=ApprovalStatusChoices.CHOICES,
        default=ApprovalStatusChoices.PENDING,
        verbose_name="Estado de Aprobación"
    )
    visibility = models.CharField(
        max_length=10,
        choices=VisibilityChoices.CHOICES,
        default=VisibilityChoices.PUBLIC,
        verbose_name="Visibilidad"
    )

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        unique_together = ('extraction_phase', 'name')  # Un nombre único por fase

    def __str__(self):
        return self.name

    # Nota: La lógica para el campo 'is_mandatory' (calculado si está relacionado a la RQ)
    # debe implementarse en la lógica de negocio (services/signals) o un método del modelo,
    # ya que no es un campo de base de datos puramente calculado.