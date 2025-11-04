# extraction/models/core.py (o un nuevo 'records.py')
from django.db import models
from django.conf import settings
from papers.models import Paper

class ExtractionPaper(models.Model):
    # Enlace 1-a-1 con el Paper. Cada paper solo tiene un registro de extracción.
    paper = models.OneToOneField(
        Paper,
        on_delete=models.CASCADE,
        related_name="extraction_record"
    )

    # Atributos del modulo de extraccion
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('InProgress', 'In Progress'), ('Done', 'Done')],
        default='Pending'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, # MEJOR PRÁCTICA
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="extraction_assignments"
    )
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Extraction Record"
        verbose_name_plural = "Extraction Records"

    def __str__(self):
        return f"{self.paper.title} - {self.status}"

