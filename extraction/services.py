from django.contrib.auth import get_user_model
from django.db import transaction

# Importaciones de modelos modulares
from projects.models import ResearchProject
from design.models import ResearchQuestion
from .models import ExtractionPhase, Tag
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


@transaction.atomic
def create_tag_with_pi(
        creator: User,
        project: ResearchProject,
        tag_name: str,
        pi_text: str = None
) -> Tag:
    """
    Caso de Uso: Un Owner define un Tag Deductivo.

    Encapsula las reglas de negocio:
    - Si un Tag se vincula a una PI, se marca como 'obligatorio'.
    - Si no se vincula, es 'opcional' (is_mandatory=False).
    """
    related_question = None
    is_mandatory = False

    if pi_text:
        try:
            # Buscamos la PI dentro del proyecto correcto
            related_question = ResearchQuestion.objects.get(
                project=project,
                text=pi_text
            )
            is_mandatory = True
        except ResearchQuestion.DoesNotExist:
            raise ValueError(f"La PI '{pi_text}' no existe en este proyecto.")

    tag = Tag.objects.create(
        name=tag_name,
        created_by=creator,
        question=related_question,
        type=Tag.TagType.DEDUCTIVE,
        is_mandatory=is_mandatory,
        is_public=True
    )

    return tag


def is_tag_list_public(project: ResearchProject) -> bool:
    """
    Caso de Uso: Determina si la lista de tags debe ser visible.

    "La lista de tags será visible siempre y cuando TODAS las
       preguntas de investigación estén siendo usadas por un tag."
    """

    has_unlinked_questions = ResearchQuestion.objects.filter(
        project=project,
        tags__isnull=True
    ).exists()

    return not has_unlinked_questions