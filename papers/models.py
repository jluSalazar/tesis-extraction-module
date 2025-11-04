from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Dependencia del módulo de proyectos. Es una dependencia de dominio válida.
from projects.models import ResearchProject

class Paper(models.Model):
    """
    Representa un documento (paper) a ser analizado.
    """
    class Status(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        IN_PROGRESS = 'InProgress', _('In Progress')
        DONE = 'Done', _('Done')

    # Un Paper debe pertenecer a un Proyecto.
    # Esta es una adición lógica al esquema propuesto.
    project = models.ForeignKey(
        ResearchProject,
        on_delete=models.CASCADE, # Si se borra el proyecto, se borran sus papers
        related_name='papers'
    )
    title = models.CharField(max_length=512) # Títulos pueden ser largos
    authors = models.CharField(max_length=1024, blank=True)
    year = models.IntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    fulltext = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Mantener el paper si el uploader se va
        null=True,
        related_name='uploaded_papers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title[:80]}... ({self.year})"