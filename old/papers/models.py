from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Dependencia del módulo de proyectos. Es una dependencia de dominio válida.
from projects.models import ResearchProject


class Paper(models.Model):
    """
    Representa un documento (papers) a ser analizado.
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
    path =  models.TextField(blank=True)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_papers'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title[:80]}... ({self.year})"