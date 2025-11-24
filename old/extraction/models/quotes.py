"""Modelo para fragmentos de texto extraídos de papers."""

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation


class QuoteQuerySet(models.QuerySet):
    """QuerySet personalizado para Quotes."""

    def validated(self):
        """Retorna quotes validadas."""
        return self.filter(validated=True)

    def unvalidated(self):
        """Retorna quotes sin validar."""
        return self.filter(validated=False)

    def by_researcher(self, user):
        """Retorna quotes de un investigador específico."""
        return self.filter(researcher=user)

    def for_extraction(self, paper_extraction):
        """
        Retorna quotes de una extracción específica.
        
        ACTUALIZADO: Usa paper_extraction en vez de paper.
        """
        return self.filter(paper_extraction=paper_extraction)
    
    def for_paper(self, paper):
        """
        Retorna quotes de un paper específico.
        
        Accede a través de la relación con PaperExtraction.
        """
        return self.filter(paper_extraction__paper=paper)

    def with_tag(self, tag):
        """Retorna quotes que tienen un tag específico."""
        return self.filter(tags=tag)

    def for_project(self, project):
        """
        Retorna quotes de un proyecto específico.
        
        ACTUALIZADO: Usa la nueva relación con PaperExtraction.
        """
        return self.filter(paper_extraction__paper__project=project)

    def prefetch_related_data(self):
        """Precarga tags, comentarios y researcher para evitar N+1."""
        return self.select_related(
            'researcher',
            'paper_extraction',
            'paper_extraction__paper'  # ← También precarga el paper
        ).prefetch_related(
            'tags',
            'comments__user'
        )


class QuoteManager(models.Manager):
    """Manager personalizado para Quotes."""

    def get_queryset(self):
        return QuoteQuerySet(self.model, using=self._db)

    def validated(self):
        return self.get_queryset().validated()

    def unvalidated(self):
        return self.get_queryset().unvalidated()

    def by_researcher(self, user):
        return self.get_queryset().by_researcher(user)

    def for_extraction(self, paper_extraction):
        return self.get_queryset().for_extraction(paper_extraction)
    
    def for_paper(self, paper):
        return self.get_queryset().for_paper(paper)

    def with_tag(self, tag):
        return self.get_queryset().with_tag(tag)

    def for_project(self, project):
        return self.get_queryset().for_project(project)


class Quote(models.Model):
    """
    Fragmento (cita) de texto extraído de un Paper.

    Esta es una entidad central en el Aggregate Root de PaperExtraction.

    🔗 RELACIÓN CON PAPEREXTRACTION:
    Quote → PaperExtraction → Paper
    
    ¿Por qué no directamente a Paper?
    - Porque Quote pertenece al CONTEXTO de extracción
    - PaperExtraction es el Aggregate Root
    - Mantiene la cohesión del bounded context

    Reglas de Negocio:
    - Toda quote debe tener al menos un tag (validado en el servicio)
    - Solo el researcher que la creó puede editarla (sin permisos especiales)
    - Una quote validada solo puede ser editada por un Owner
    """

    text_portion = models.TextField(
        help_text="Fragmento textual extraído del paper"
    )
    
    # ACTUALIZADO: FK a PaperExtraction en vez de ExtractionRecord
    paper_extraction = models.ForeignKey(
        'old.extraction.PaperExtraction',
        on_delete=models.CASCADE,
        related_name='quotes',
        help_text="Extracción a la que pertenece esta quote"
    )
    
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ubicación en el paper (página, sección, etc.)"
    )
    tags = models.ManyToManyField(
        'old.extraction.Tag',
        related_name='quotes',
        blank=True
    )
    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='quotes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(
        default=False,
        help_text="Indica si la quote ha sido validada por un revisor"
    )

    comments = GenericRelation(
        'extraction.Comment',
        related_query_name='quote'
    )

    objects = QuoteManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['validated', 'created_at']),
            models.Index(fields=['researcher', 'created_at']),
            models.Index(fields=['paper_extraction', 'validated']),
        ]
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"

    def __str__(self):
        preview = self.text_portion[:100]
        return f'"{preview}..." by {self.researcher.username}'
    
    # ================================================
    # 🔑 PROXY PROPERTIES (Igual que en PaperExtraction)
    # ================================================
    
    @property
    def paper(self):
        """
        Acceso directo al Paper.
        
        Proxy: quote.paper en vez de quote.paper_extraction.paper
        """
        return self.paper_extraction.paper
    
    @property
    def project(self):
        """
        Acceso directo al proyecto.
        
        Proxy profundo:
        - Sin proxy: quote.paper_extraction.paper.project
        - Con proxy: quote.project
        """
        return self.paper_extraction.project

    @property
    def has_mandatory_tags(self):
        """Verifica si tiene todos los tags obligatorios del proyecto."""
        from .tags import Tag
        
        # ✅ Usa el proxy property 'project'
        mandatory_tags = Tag.objects.filter(
            question__project=self.project,
            is_mandatory=True
        )

        quote_mandatory_tags = self.tags.filter(is_mandatory=True)
        return quote_mandatory_tags.count() >= mandatory_tags.count()