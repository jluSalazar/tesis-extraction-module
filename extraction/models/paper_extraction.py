# ================================================
# FILE: extraction/models/paper_extraction.py
# ================================================
"""
Modelo para tracking del estado de extracción de cada paper.

Este modelo extiende la funcionalidad del modelo Paper de otra app
sin modificar directamente ese modelo (Open/Closed Principle).

Patrón: Extension Model / Proxy Attributes
Nombre anterior: ExtractionRecord
Nuevo nombre: PaperExtraction (más descriptivo del propósito)
"""

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from papers.models import Paper


class PaperExtractionQuerySet(models.QuerySet):
    """QuerySet personalizado para PaperExtraction."""
    
    def pending(self):
        """Retorna registros pendientes."""
        return self.filter(status=PaperExtraction.Status.PENDING)
    
    def in_progress(self):
        """Retorna registros en progreso."""
        return self.filter(status=PaperExtraction.Status.IN_PROGRESS)
    
    def completed(self):
        """Retorna registros completados."""
        return self.filter(status=PaperExtraction.Status.DONE)
    
    def for_user(self, user):
        """Retorna registros asignados a un usuario."""
        return self.filter(assigned_to=user)
    
    def pending_for_user(self, user):
        """
        Retorna registros pendientes para un usuario específico.
        Optimizada con select_related para evitar N+1 queries.
        """
        return self.filter(
            assigned_to=user,
            status=PaperExtraction.Status.PENDING
        ).select_related('paper', 'assigned_to')
    
    def for_project(self, project):
        """Retorna registros de un proyecto específico."""
        return self.filter(paper__project=project)
    
    def unassigned(self):
        """Retorna registros sin asignar."""
        return self.filter(assigned_to__isnull=True)
    
    def with_missing_tags(self):
        """
        Retorna registros que tienen tags obligatorios faltantes.
        """
        return self.filter(extraction_errors__is_resolved=False).distinct()
    
    def ready_to_complete(self):
        """
        Retorna registros que están listos para marcarse como completados.
        """
        return self.filter(
            status=PaperExtraction.Status.IN_PROGRESS
        ).exclude(
            extraction_errors__is_resolved=False
        )


class PaperExtractionManager(models.Manager):
    """Manager personalizado para PaperExtraction."""
    
    def get_queryset(self):
        return PaperExtractionQuerySet(self.model, using=self._db)
    
    def pending(self):
        return self.get_queryset().pending()
    
    def in_progress(self):
        return self.get_queryset().in_progress()
    
    def completed(self):
        return self.get_queryset().completed()
    
    def for_user(self, user):
        return self.get_queryset().for_user(user)
    
    def pending_for_user(self, user):
        return self.get_queryset().pending_for_user(user)
    
    def for_project(self, project):
        return self.get_queryset().for_project(project)
    
    def unassigned(self):
        return self.get_queryset().unassigned()
    
    def create_for_paper(self, paper, assigned_to=None):
        """
        Factory method para crear un PaperExtraction.
        Asegura consistencia en la creación.
        """
        return self.create(
            paper=paper,
            assigned_to=assigned_to,
            status=self.model.Status.PENDING
        )


class PaperExtraction(models.Model):
    """
    Extiende Paper con atributos específicos del proceso de extracción.
    
    🎯 PROPÓSITO:
    Este modelo NO es una copia de Paper ni un Paper "mejorado".
    Es una EXTENSIÓN que agrega SOLO los atributos que pertenecen
    al CONTEXTO de extracción, sin modificar el modelo Paper original.
    
    📦 PATRÓN: Extension Model (Django Best Practice)
    
    🔗 RELACIÓN: OneToOne con Paper
    - Un Paper puede existir sin PaperExtraction (no todos se extraen)
    - Un PaperExtraction SIEMPRE pertenece a un Paper
    
    🔑 ACCESO DESDE PAPER:
        paper = Paper.objects.get(id=1)
        paper.extraction  # ← Retorna este modelo
        paper.extraction.status
        paper.extraction.assigned_to
    
    🔑 ACCESO DESDE PAPEREXTRACTION (Proxy Properties):
        extraction = PaperExtraction.objects.get(id=1)
        extraction.title     # ← Proxy a paper.title
        extraction.authors   # ← Proxy a paper.authors
        extraction.project   # ← Proxy a paper.project

    🔐 REGLAS DE NEGOCIO:
    - Solo puede marcarse como 'Done' si tiene todas las extracciones obligatorias
    - Un paper con estado 'Done' no puede editarse (sin permisos especiales)
    - Solo puede crearse si el proyecto tiene fase activa
    - Solo el researcher asignado puede trabajar en el record
    """
    
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pendiente'
        IN_PROGRESS = 'InProgress', 'En Progreso'
        DONE = 'Done', 'Completado'
    
    # --- Relación 1-to-1 con Paper (Extension Pattern) ---
    paper = models.OneToOneField(
        Paper,
        on_delete=models.CASCADE,
        related_name='extraction',  # paper.extraction (nombre más corto)
        help_text="Paper al que pertenece este registro de extracción"
    )
    
    # --- Atributos Específicos de Extracción ---
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paper_extractions',  # user.paper_extractions
        help_text="Researcher asignado a este paper"
    )
    
    # --- Tracking Temporal ---
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha en que se cambió el estado a 'In Progress'"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha en que se marcó como 'Done'"
    )
    
    # --- Metadata Adicional ---
    notes = models.TextField(
        blank=True,
        help_text="Notas internas del researcher sobre este paper"
    )
    
    objects = PaperExtractionManager()

    class Meta:
        verbose_name = "Paper Extraction"
        verbose_name_plural = "Paper Extractions"
        ordering = ['-last_modified']
        indexes = [
            models.Index(fields=['status', 'assigned_to']),
            models.Index(fields=['status', 'last_modified']),
            models.Index(fields=['assigned_to', 'status']),
        ]

    def __str__(self):
        return f"{self.paper.title} - {self.get_status_display()}"
    
    # ================================================
    # 🔑 PROXY PROPERTIES
    # Acceso directo a atributos del Paper relacionado
    # ================================================
    
    @property
    def title(self):
        """
        Acceso directo al título del paper.
        
        Uso:
            extraction.title  # En vez de: extraction.paper.title
        """
        return self.paper.title
    
    @property
    def authors(self):
        """
        Acceso directo a los autores del paper.
        
        Uso:
            extraction.authors  # En vez de: extraction.paper.authors
        """
        return self.paper.authors
    
    @property
    def year(self):
        """Acceso directo al año del paper."""
        return self.paper.year
    
    @property
    def project(self):
        """
        Acceso directo al proyecto del paper.
        
        IMPORTANTE: Este es un proxy MUY útil porque evita:
            extraction.paper.project  (2 niveles)
        
        Con el proxy:
            extraction.project  (1 nivel)
        """
        return self.paper.project
    
    @property
    def project_name(self):
        """
        Acceso directo al nombre del proyecto.
        
        Ejemplo de proxy "profundo" - atraviesa múltiples relaciones:
        Sin proxy: extraction.paper.project.title
        Con proxy: extraction.project_name
        """
        return self.paper.project.title
    
    # ================================================
    # 🎯 BUSINESS LOGIC PROPERTIES
    # Encapsulan lógica de negocio específica
    # ================================================
    
    @property
    def is_pending(self):
        """Verifica si el registro está pendiente."""
        return self.status == self.Status.PENDING
    
    @property
    def is_in_progress(self):
        """Verifica si el registro está en progreso."""
        return self.status == self.Status.IN_PROGRESS
    
    @property
    def is_completed(self):
        """Verifica si el registro está completado."""
        return self.status == self.Status.DONE
    
    @property
    def has_quotes(self):
        """Verifica si tiene quotes asociadas."""
        return self.quotes.exists()
    
    @property
    def quote_count(self):
        """Retorna el número de quotes extraídas."""
        return self.quotes.count()
    
    @property
    def has_errors(self):
        """Verifica si tiene errores sin resolver."""
        return self.extraction_errors.filter(is_resolved=False).exists()
    
    @property
    def can_be_completed(self):
        """
        Verifica si el registro puede marcarse como completado.
        
        Requisitos:
        - Debe tener al menos una quote
        - No debe tener errores sin resolver
        - Debe estar en estado 'In Progress'
        """
        return (
            self.is_in_progress and
            self.has_quotes and
            not self.has_errors
        )
    
    @property
    def progress_percentage(self):
        """
        Calcula el porcentaje de progreso basado en tags obligatorios.
        
        Returns:
            float: Porcentaje de 0 a 100
        """
        from .tags import Tag
        
        mandatory_tags = Tag.objects.filter(
            question__project=self.project,
            is_mandatory=True
        )
        
        if not mandatory_tags.exists():
            return 100.0 if self.has_quotes else 0.0
        
        tags_with_quotes = 0
        for tag in mandatory_tags:
            if self.quotes.filter(tags=tag).exists():
                tags_with_quotes += 1
        
        return (tags_with_quotes / mandatory_tags.count()) * 100
    
    # ================================================
    # ✅ VALIDATIONS
    # ================================================
    
    def clean(self):
        """Validaciones a nivel de modelo."""
        super().clean()
        
        if self.status == self.Status.DONE and not self.has_quotes:
            raise ValidationError(
                "No se puede marcar como completado un registro sin quotes."
            )
        
        if self.status == self.Status.DONE and self.has_errors:
            raise ValidationError(
                "No se puede marcar como completado con errores sin resolver."
            )
    
    def save(self, *args, **kwargs):
        """Override save para aplicar lógica automática."""
        # Auto-actualizar timestamps según el estado
        if self.status == self.Status.IN_PROGRESS and not self.started_at:
            from django.utils import timezone
            self.started_at = timezone.now()
        
        if self.status == self.Status.DONE and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    # ================================================
    # 🔧 BUSINESS METHODS
    # ================================================
    
    def start_extraction(self, user):
        """Marca el registro como 'In Progress'."""
        if not self.is_pending:
            raise ValidationError(
                f"Solo se puede iniciar extracción de registros pendientes. "
                f"Estado actual: {self.get_status_display()}"
            )
        
        from django.utils import timezone
        self.status = self.Status.IN_PROGRESS
        self.started_at = timezone.now()
        self.save()
    
    def mark_as_complete(self):
        """Marca el registro como completado."""
        if not self.can_be_completed:
            errors = []
            if not self.is_in_progress:
                errors.append(f"Estado: {self.get_status_display()}")
            if not self.has_quotes:
                errors.append("Sin quotes")
            if self.has_errors:
                errors.append("Errores sin resolver")
            
            raise ValidationError(
                f"No se puede completar. Problemas: {', '.join(errors)}"
            )
        
        from django.utils import timezone
        self.status = self.Status.DONE
        self.completed_at = timezone.now()
        self.save()
    
    def reopen(self):
        """Reabre un registro completado."""
        if not self.is_completed:
            raise ValidationError("Solo se pueden reabrir registros completados.")
        
        self.status = self.Status.IN_PROGRESS
        self.completed_at = None
        self.save()


# ================================================
# 📡 SIGNALS (Opcional)
# ================================================

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Paper)
def create_extraction_for_new_paper(sender, instance, created, **kwargs):
    """
    Crea automáticamente un PaperExtraction cuando se crea un Paper.
    
    NOTA: Solo si el proyecto tiene fase de extracción activa.
    """
    if created:
        try:
            extraction_phase = instance.project.extraction_phase
            if extraction_phase.is_active:
                PaperExtraction.objects.create_for_paper(paper=instance)
        except AttributeError:
            pass
