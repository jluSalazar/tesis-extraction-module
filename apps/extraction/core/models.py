from django.db import models
from django.contrib.auth import get_user_model


from ..external.models import Study
from ..shared.audit import AuditModel
from ..planning.models import ExtractionPhase
from ..taxonomy.models import Tag

User = get_user_model()


class TagTypeChoices:
    """Opciones para el tipo de Tag."""
    DEDUCTIVE = 'DEDUCTIVE'
    INDUCTIVE = 'INDUCTIVE'

    CHOICES = [
        (DEDUCTIVE, 'Deductiva'),
        (INDUCTIVE, 'Inductiva'),
    ]


class PaperExtractionStatusChoices:
    """Opciones para el estado de PaperExtraction."""
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'

    CHOICES = [
        (PENDING, 'Pendiente'),
        (IN_PROGRESS, 'En Progreso'),
        (COMPLETED, 'Completado'),
    ]


class PaperExtraction(AuditModel):
    """Representa un archivo PDF o documento de donde se extraerá la información."""

    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE,
        related_name='paper_extractions',
        verbose_name="Estudio Relacionado (Acquisition)"
    )
    status = models.CharField(
        max_length=15,
        choices=PaperExtractionStatusChoices.CHOICES,
        default=PaperExtractionStatusChoices.PENDING,
        verbose_name="Estado de la Extracción"
    )
    extraction_phase = models.ForeignKey(
        ExtractionPhase,
        on_delete=models.CASCADE,
        related_name='papers_to_extract',
        verbose_name="Fase de Extracción"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_extractions',
        verbose_name="Asignado A"
    )
    # Usar FilePathField o FileField, dependiendo de si el archivo se sube o se referencia.
    path = models.CharField(max_length=500, verbose_name="Ruta o URL del Documento")

    class Meta:
        verbose_name = "Extracción de Paper"
        verbose_name_plural = "Extracciones de Papers"
        # Un paper puede ser asignado a una fase una sola vez
        unique_together = ('study', 'extraction_phase')

    def __str__(self):
        return f"Extracción de {self.study.title} en {self.extraction_phase.project.name}"


# =================================================================
# 3. Entidad Hija (Quote - contenida en PaperExtraction)
# =================================================================

class Quote(AuditModel):
    """Extracciones de texto (citas) de un documento (PaperExtraction)."""

    text_fragment = models.TextField(verbose_name="Fragmento de Texto Extraído")
    # Usa JSONField para almacenar la ubicación estructurada
    location = models.JSONField(
        default=dict,
        verbose_name="Ubicación (Página, Párrafo, etc.)"
    )
    paper_extraction = models.ForeignKey(
        PaperExtraction,
        on_delete=models.CASCADE,
        related_name='quotes',
        verbose_name="Paper de Origen"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='quotes',
        verbose_name="Etiquetas Aplicadas"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_quotes',
        verbose_name="Creado Por"
    )

    class Meta:
        verbose_name = "Cita de Extracción"
        verbose_name_plural = "Citas de Extracción"
        # Ordenar las citas por fecha de creación o ID
        ordering = ['created_at']

    def __str__(self):
        # Muestra los primeros 50 caracteres del fragmento
        return f"Cita de '{self.text_fragment[:50]}...' de {self.paper_extraction.study.title}"