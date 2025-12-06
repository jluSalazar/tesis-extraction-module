from django.db import models
from django.contrib.auth import get_user_model
from ..external.models import Project
from ..shared.audit import AuditModel

User = get_user_model()

class ExtractionStatusChoices:
    """Opciones para el estado de ExtractionPhase."""
    CONFIG = 'CONFIG'
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

    CHOICES = [
        (CONFIG, 'Configuración'),
        (OPEN, 'Abierta'),
        (CLOSED, 'Cerrada'),
    ]


class ExtractionPhase(AuditModel):
    """Modelo principal que define la configuración y el ciclo de vida de la extracción."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='extraction_phases',
        verbose_name="Proyecto Relacionado"
    )
    status = models.CharField(
        max_length=10,
        choices=ExtractionStatusChoices.CHOICES,
        default=ExtractionStatusChoices.CONFIG,
        verbose_name="Estado de la Fase"
    )
    is_tag_list_visible = models.BooleanField(
        default=True,
        verbose_name="Visibilidad de la Lista de Etiquetas"
    )

    start_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
    due_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")

    class Meta:
        verbose_name = "Fase de Extracción"
        verbose_name_plural = "Fases de Extracción"
        # Restricción para asegurar una fase por proyecto, si es necesario
        # unique_together = ('project',)

    def __str__(self):
        return f"Fase de Extracción de: {self.project.name} ({self.status})"