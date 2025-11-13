"""Modelo de comentarios genéricos para Quotes y Tags."""

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentQuerySet(models.QuerySet):
    """QuerySet personalizado para Comments."""

    def reviews(self):
        """Retorna solo comentarios de revisión."""
        return self.filter(is_review=True)

    def regular(self):
        """Retorna comentarios regulares (no revisiones)."""
        return self.filter(is_review=False)

    def by_user(self, user):
        """Retorna comentarios de un usuario específico."""
        return self.filter(user=user)

    def for_model(self, model_class):
        """Retorna comentarios de un tipo de modelo específico."""
        content_type = ContentType.objects.get_for_model(model_class)
        return self.filter(content_type=content_type)


class CommentManager(models.Manager):
    """Manager personalizado para Comments."""

    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def reviews(self):
        return self.get_queryset().reviews()

    def regular(self):
        return self.get_queryset().regular()

    def by_user(self, user):
        return self.get_queryset().by_user(user)

    def for_model(self, model_class):
        return self.get_queryset().for_model(model_class)


class Comment(models.Model):
    """
    Comentarios generales que pueden asociarse a diferentes entidades
    mediante GenericForeignKey (quotes, tags, etc.)

    Uso:
        # Comentario en Quote
        comment = Comment.objects.create(
            user=user,
            content_object=quote,
            text="Mi interpretación..."
        )

        # Comentario en Tag
        comment = Comment.objects.create(
            user=user,
            content_object=tag,
            text="Justificación adicional..."
        )
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='extraction_comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_review = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Indica si es parte de una revisión formal"
    )

    # Relación genérica - permite asociar a cualquier modelo
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = CommentManager()

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['is_review', 'created_at']),
        ]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

