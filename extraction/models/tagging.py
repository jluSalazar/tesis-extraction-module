from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Dependencia del módulo central 'protocol'
from design.models import ResearchQuestion

class Tag(models.Model):
    """
    Representa un Tag (o "código") que puede ser aplicado a las Quotes.
    """

    class TagType(models.TextChoices):
        DEDUCTIVE = 'deductive', _('Deductivo')
        INDUCTIVE = 'inductive', _('Inductivo')

    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, default='#FFFFFF', blank=True)
    justification = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tags'
    )
    question = models.ForeignKey(
        ResearchQuestion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tags'
    )
    type = models.CharField(
        max_length=20,
        choices=TagType.choices,
        default=TagType.DEDUCTIVE
    )
    is_mandatory = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    # Relación genérica inversa para comentarios
    comments = GenericRelation(Comment, related_query_name='tag')

    def __str__(self):
        return self.name