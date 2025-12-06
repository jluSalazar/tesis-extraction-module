from django.db import models
#from ..core.models import AuditModel


class Project(models.Model):
    """Define un proyecto de investigación o revisión sistemática."""

    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('PAUSED', 'Pausado'),
        ('COMPLETED', 'Completado'),
        ('ARCHIVED', 'Archivado'),
    ]

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Nombre del Proyecto"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descripción"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name="Estado del Proyecto"
    )

    # Otros campos relacionados con la gestión de proyectos...

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.name


class ResearchQuestion(models.Model):
    """Preguntas de investigación definidas para un proyecto."""

    question_text = models.TextField(
        verbose_name="Texto de la Pregunta"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='research_questions',
        verbose_name="Proyecto Relacionado"
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Es Pregunta Primaria"
    )

    class Meta:
        verbose_name = "Pregunta de Investigación"
        verbose_name_plural = "Preguntas de Investigación"
        # La pregunta debe ser única dentro del proyecto
        unique_together = ('project', 'question_text')

    def __str__(self):
        return self.question_text[:100]



class Study(models.Model):
    """Representa un estudio o artículo adquirido para la revisión."""

    title = models.CharField(
        max_length=500,
        verbose_name="Título del Estudio"
    )
    authors = models.CharField(
        max_length=500,
        verbose_name="Autores"
    )
    publication_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Año de Publicación"
    )
    # Enlace al proyecto para el que se adquirió el estudio
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='acquired_studies',
        verbose_name="Proyecto Relacionado"
    )
    # URL o DOI, para referencia
    reference_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="DOI/URL de Referencia"
    )

    class Meta:
        verbose_name = "Estudio Adquirido"
        verbose_name_plural = "Estudios Adquiridos"
        # Se podría considerar unique_together en (project, title) o (DOI)

    def __str__(self):
        return self.title