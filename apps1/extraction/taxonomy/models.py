"""Modelo para tags (códigos) aplicables a quotes."""

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from design.models import ResearchQuestion


class TagQuerySet(models.QuerySet):
    """QuerySet personalizado para Tags."""

    def public(self):
        """Retorna solo tags públicos."""
        return self.filter(is_public=True)

    def mandatory(self):
        """Retorna solo tags obligatorios."""
        return self.filter(is_mandatory=True)

    def optional(self):
        """Retorna solo tags opcionales."""
        return self.filter(is_mandatory=False)

    def deductive(self):
        """Retorna solo tags deductivos."""
        return self.filter(type=Tag.TagType.DEDUCTIVE)

    def inductive(self):
        """Retorna solo tags inductivos."""
        return self.filter(type=Tag.TagType.INDUCTIVE)

    def for_project(self, project):
        """Retorna tags de un proyecto específico."""
        return self.filter(question__project=project)

    def for_question(self, question):
        """Retorna tags vinculados a una pregunta específica."""
        return self.filter(question=question)

    def without_question(self):
        """Retorna tags sin pregunta de investigación (inductivos)."""
        return self.filter(question__isnull=True)

    def with_usage_count(self):
        """Anota el número de veces que se ha usado cada tag."""
        return self.annotate(usage_count=models.Count('quotes'))


class TagManager(models.Manager):
    """Manager personalizado para Tags."""

    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def public(self):
        return self.get_queryset().public()

    def mandatory(self):
        return self.get_queryset().mandatory()

    def optional(self):
        return self.get_queryset().optional()

    def deductive(self):
        return self.get_queryset().deductive()

    def inductive(self):
        return self.get_queryset().inductive()

    def for_project(self, project):
        return self.get_queryset().for_project(project)

    def for_question(self, question):
        return self.get_queryset().for_question(question)


class Tag(models.Model):
    """
    Representa un Tag (código) que puede ser aplicado a las Quotes.

    Tipos de Tags:
    - DEDUCTIVE: Definidos a priori basados en preguntas de investigación
    - INDUCTIVE: Emergentes del análisis de los datos

    Reglas de Negocio:
    - Si tiene 'question' → is_mandatory=True (Regla #10)
    - Si no tiene 'question' → is_mandatory=False (Regla #11)
    - Solo el Owner puede crear/modificar tags deductivos (Regla #7)
    - Tags con quotes asociadas no pueden eliminarse
    """

    class TagType(models.TextChoices):
        DEDUCTIVE = 'deductive', _('Deductivo')
        INDUCTIVE = 'inductive', _('Inductivo')

    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=50,
        default='#FFFFFF',
        blank=True,
        help_text="Color hexadecimal para visualización"
    )
    justification = models.TextField(
        blank=True,
        help_text="Definición y criterios de aplicación del tag"
    )
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
        related_name='tags',
        help_text="Pregunta de investigación asociada (si es deductivo)"
    )
    type = models.CharField(
        max_length=20,
        choices=TagType.choices,
        default=TagType.DEDUCTIVE
    )
    is_mandatory = models.BooleanField(
        default=False,
        help_text="Si es obligatorio aplicar este tag (automático si tiene question)"
    )
    is_public = models.BooleanField(
        default=True,
        help_text="Si es visible para los investigadores"
    )

    # Relación genérica inversa para comentarios
    comments = GenericRelation(
        'extraction.Comment',
        related_query_name='tag'
    )

    objects = TagManager()

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['type', 'is_mandatory']),
            models.Index(fields=['is_public', 'type']),
        ]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        # Evita tags duplicados por nombre en el mismo proyecto
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'question'],
                name='unique_tag_name_per_question'
            )
        ]

    def __str__(self):
        type_label = "D" if self.type == self.TagType.DEDUCTIVE else "I"
        return f"[{type_label}] {self.name}"

    @property
    def usage_count(self):
        """Retorna el número de quotes que usan este tag."""
        return self.quotes.count()

