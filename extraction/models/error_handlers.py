"""Modelo para manejo de errores y notificaciones de validación."""

from django.db import models
from django.conf import settings


class ErrorHandlerQuerySet(models.QuerySet):
    """QuerySet personalizado para ErrorHandler."""

    def unresolved(self):
        """Retorna errores no resueltos."""
        return self.filter(is_resolved=False)

    def resolved(self):
        """Retorna errores resueltos."""
        return self.filter(is_resolved=True)

    def unsent(self):
        """Retorna errores sin enviar."""
        return self.filter(sent_at__isnull=True)

    def sent(self):
        """Retorna errores enviados."""
        return self.filter(sent_at__isnull=False)

    def for_user(self, user):
        """Retorna errores de un usuario específico."""
        return self.filter(user=user)

    def for_paper(self, paper):
        """Retorna errores de un paper específico."""
        return self.filter(paper=paper)


class ErrorHandlerManager(models.Manager):
    """Manager personalizado para ErrorHandler."""

    def get_queryset(self):
        return ErrorHandlerQuerySet(self.model, using=self._db)

    def unresolved(self):
        return self.get_queryset().unresolved()

    def resolved(self):
        return self.get_queryset().resolved()

    def unsent(self):
        return self.get_queryset().unsent()

    def sent(self):
        return self.get_queryset().sent()

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def for_paper(self, paper):
        return self.get_queryset().for_paper(paper)


class ErrorHandler(models.Model):
    """
    Registra y notifica errores de validación en la extracción.

    Casos de uso:
    - Falta de tags obligatorios (Regla #12)
    - Intento de operación en fase cerrada (Regla #16)
    - Violación de reglas de negocio

    Reglas de Negocio:
    - Se crea automáticamente cuando falta un tag obligatorio
    - Se marca como resuelto cuando se corrige el error
    - Las notificaciones se envían al researcher asignado
    """

    paper = models.ForeignKey(
        'extraction.PaperExtraction',  # String reference
        on_delete=models.CASCADE,
        related_name='extraction_errors'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='extraction_errors',
        help_text="Usuario que debe ser notificado"
    )
    missing_tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de tags obligatorios que faltan"
    )
    message = models.TextField(
        help_text="Mensaje descriptivo del error"
    )
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Fecha en que se envió la notificación"
    )
    is_resolved = models.BooleanField(
        default=False,
        help_text="Indica si el error ha sido corregido"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ErrorHandlerManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_resolved', 'created_at']),
            models.Index(fields=['user', 'is_resolved']),
        ]
        verbose_name = "Error Handler"
        verbose_name_plural = "Error Handlers"

    def __str__(self):
        status = "Resolved" if self.is_resolved else "Unresolved"
        return f"[{status}] Error on {self.paper.paper.title} for {self.user.username}"