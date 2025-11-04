from django.db import models
from django.conf import settings

# Dependencia del módulo central 'papers'
from papers.models import Paper

class ErrorHandler(models.Model):
    """
    Registra y notifica errores de validación en la extracción,
    como la falta de tags mandatorios.
    """
    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        related_name='extraction_errors'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Errores asociados al usuario notificado
        related_name='extraction_errors'
    )
    missing_tags = models.JSONField(default=list, blank=True)
    message = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True, db_index=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Error en Paper {self.paper_id} para {self.user.username}"