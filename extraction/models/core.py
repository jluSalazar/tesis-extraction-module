from django.db import models
from django.conf import settings

# Dependencias
from papers.models import Paper # Módulo central
from .tagging import Tag        # Módulo local (dentro de la app)

class Quote(models.Model):
    """
    Fragmento (cita) de texto extraído de un Paper.
    Esta es una entidad central en el Aggregate Root de Paper.
    """
    text_portion = models.TextField()
    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE, # Si se borra el Paper, sus Quotes se van
        related_name='quotes'
    )
    location = models.CharField(max_length=100, blank=True)
    comment = models.TextField(
        blank=True,
        help_text="Interpretación o nota inicial del investigador."
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='quotes',
        blank=True
    )
    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Proteger la data generada por el investigador
        related_name='quotes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)
    version = models.IntegerField(default=1) # Para control de concurrencia

    def __str__(self):
        return f"\"{self.text_portion[:100]}...\""

    class Meta:
        ordering = ['created_at']


class Comment(models.Model):
    """
    Comentario o revisión sobre una Quote específica.
    Forma parte del agregado de Quote.
    """
    quote = models.ForeignKey(
        Quote,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Los comentarios se van con el usuario
        related_name='extraction_comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_review = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"Comentario de {self.user.username} en Quote {self.quote_id}"

    class Meta:
        ordering = ['created_at']