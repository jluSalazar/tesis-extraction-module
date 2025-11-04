from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class ResearchProject(models.Model):
    """
    Representa el proyecto de investigación o revisión sistemática.
    Es la entidad raíz para la mayoría de las operaciones.
    """
    class Status(models.TextChoices):
        DRAFT = 'Draft', _('Draft')
        EXTRACTION_ACTIVE = 'ExtractionActive', _('Extraction Active')
        CLOSED = 'Closed', _('Closed')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evitar borrado de proyecto si el owner se elimina
        related_name='owned_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True # Indexamos para búsquedas por estado
    )

    def __str__(self):
        return self.title