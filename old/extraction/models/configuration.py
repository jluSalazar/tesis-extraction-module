"""Configuración de la fase de extracción."""

from django.db import models
from projects.models import ResearchProject


class ExtractionPhase(models.Model):
    """
    Configuración de la fase de extracción para un Proyecto específico.

    Reglas de Negocio:
    - Solo puede haber una fase activa por proyecto
    - Si auto_close=True, se cierra automáticamente al alcanzar end_date
    - double_extraction requiere dos investigadores por paper
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

    class Meta:
        verbose_name = "Extraction Phase"
        verbose_name_plural = "Extraction Phases"
        ordering = ['-created_at']

    def __str__(self):
        return f"Extraction Phase: {self.project.title}"