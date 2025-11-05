from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Dependencia del módulo de proyectos. Es una dependencia de dominio válida.
from projects.models import ResearchProject


class Paper(models.Model):
    """
    Representa un documento (paper) a ser analizado.
    """
    # ... (project, title, authors, year, etc. se mantienen igual) ...
    project = models.ForeignKey(
        ResearchProject,
        on_delete=models.CASCADE,
        related_name='papers'
    )
    title = models.CharField(max_length=512)
    authors = models.CharField(max_length=1024, blank=True)
    year = models.IntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    fulltext = models.TextField(blank=True)

    # --- CAMPO AÑADIDO AQUÍ ---
    # Este campo faltaba en tu modelo pero la factory lo estaba proveyendo.
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Mantener el paper si el uploader se va
        null=True,
        related_name='uploaded_papers'
    )
    # --- FIN DEL CAMPO AÑADIDO ---

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title[:80]}... ({self.year})"