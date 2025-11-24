from django.db import models
from django.conf import settings
from papers.models import Paper
from extraction.taxonomy.models import Tag  # Dependencia entre módulos (permitida si es necesaria)


class PaperExtraction(models.Model):
    """Aggregate Root del proceso de extracción."""

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pendiente'
        IN_PROGRESS = 'InProgress', 'En Progreso'
        DONE = 'Done', 'Completado'

    paper = models.OneToOneField(Paper, on_delete=models.CASCADE, related_name='extraction')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    # 🧠 Business Logic Properties
    @property
    def is_complete(self):
        return self.status == self.Status.DONE

    def can_be_finalized(self, mandatory_tags_ids: list[int]) -> bool:
        """
        Verifica si cumple las reglas para cerrarse.
        Recibe IDs externos para no acoplarse fuertemente a la query de Tags aquí.
        """
        if not self.quotes.exists():
            return False

        # Obtener IDs de tags usados en este paper
        used_tags = set(self.quotes.values_list('tags__id', flat=True))

        # Verificar que todos los obligatorios estén presentes
        return set(mandatory_tags_ids).issubset(used_tags)

