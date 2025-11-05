from django.contrib.auth import get_user_model
from .models import ExtractionRecord  # Importa desde el __init__.py

User = get_user_model()


def get_pending_extractions(user: User):
    """
    Caso de Uso: Obtener la lista de extracciones pendientes
    para un investigador específico.

    Delega la lógica de la consulta al Manager del modelo.
    """
    # Si hubiera más lógica (ej. registrar un log, verificar permisos),
    # iría aquí.

    # Llama a nuestro "Repositorio" (el Manager)
    return ExtractionRecord.objects.get_pending_for_user(user)