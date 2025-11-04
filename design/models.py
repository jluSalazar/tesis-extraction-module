from django.db import models
from projects.models import ResearchProject

class ResearchQuestion(models.Model):
    """
    Pregunta de investigación definida en el protocolo del proyecto.
    """
    # Asumimos que la especificación de "project_id" y "id" era conceptual.
    # En Django, implementamos esto con un id automático y una FK.
    project = models.ForeignKey(
        ResearchProject,
        on_delete=models.CASCADE,
        related_name='research_questions'
    )
    text = models.TextField()

    def __str__(self):
        return self.text[:120]