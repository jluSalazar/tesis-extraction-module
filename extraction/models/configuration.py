from django.db import models

# Dependencia del módulo central 'projects'
from projects.models import ResearchProject


class Extraction(models.Model):
    """
    Configuración de la fase de extracción para un Proyecto específico.
    """
    # Esta es una adición lógica clave. Una configuración de extracción
    # no puede existir sin un proyecto. Usamos OneToOneField porque
    # solo hay UNA configuración de extracción por proyecto.
    project = models.OneToOneField(
        ResearchProject,
        on_delete=models.CASCADE,
        related_name='extraction_config'
    )

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    double_extraction = models.BooleanField(default=False)
    auto_close = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Configuración de Extracción para: {self.project.title}"