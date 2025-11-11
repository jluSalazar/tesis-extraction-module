from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

# Dependencias
from .records import ExtractionRecord
from design.models import ResearchQuestion


class Comment(models.Model):
    """
    Comentarios generales que pueden asociarse a diferentes entidades
    mediante GenericForeignKey (quotes, tags, etc.)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='extraction_comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_review = models.BooleanField(default=False, db_index=True)

    # Relación genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Comentario de {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]


class Quote(models.Model):
    """
    Fragmento (cita) de texto extraído de un Paper.
    Esta es una entidad central en el Aggregate Root de Paper.
    """
    text_portion = models.TextField()
    paper = models.ForeignKey(
        ExtractionRecord,
        on_delete=models.CASCADE,
        related_name='quotes'
    )
    location = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(
        'Tag',
        related_name='quotes',
        blank=True
    )
    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='quotes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)

    # Relación genérica inversa para comentarios
    comments = GenericRelation(Comment, related_query_name='quote')

    def __str__(self):
        return f"\"{self.text_portion[:100]}...\""

    class Meta:
        ordering = ['created_at']