from django.db import models

# Dependencia del módulo central 'projects'
from projects.models import ResearchProject


class ExtractionPhase(models.Model):
    """
    Configuración de la fase de extracción para un Proyecto específico.
    """

    project = models.OneToOneField(
        ResearchProject,
        on_delete=models.CASCADE,
        related_name='extraction_phase'
    )

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    double_extraction = models.BooleanField(default=False)
    auto_close = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fase de Extracción para: {self.project.title}"