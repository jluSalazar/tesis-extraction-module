# extraction/models/core.py (o un nuevo 'records.py')
from django.db import models
from django.conf import settings
from papers.models import Paper


# --- 1. QuerySet (Mejor Práctica para lógica reutilizable) ---
class ExtractionRecordQuerySet(models.QuerySet):

    def get_pending_for_user(self, user):
        """
        Retorna los registros de extracción pendientes para un usuario específico.
        - Optimizada con select_related para evitar N+1 queries.
        """
        # Esta es la lógica de negocio de la consulta
        return self.filter(
            assigned_to=user,
            status='Pending'
        ).select_related('paper')  # JOIN con la tabla de papers


# --- 2. Manager ---
class ExtractionRecordManager(models.Manager):

    def get_queryset(self):
        return ExtractionRecordQuerySet(self.model, using=self._db)

    def get_pending_for_user(self, user):
        """
        Expone el método del QuerySet al 'objects'.
        """
        return self.get_queryset().get_pending_for_user(user)

class ExtractionRecord(models.Model):
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

    objects = ExtractionRecordManager()

    class Meta:
        verbose_name = "Extraction Record"
        verbose_name_plural = "Extraction Records"

    def __str__(self):
        return f"{self.paper.title} - {self.status}"

