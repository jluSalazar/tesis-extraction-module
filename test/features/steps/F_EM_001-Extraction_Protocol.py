# ================================================
# FILE: extraction/tests/steps/tag_management_steps.py
# ================================================
"""
BDD Steps para gestión de tags deductivos e inductivos.

Refactorizado para usar:
- Nueva estructura de servicios separados
- PaperExtraction en vez de ExtractionRecord
- Mejores prácticas de testing
"""

from behave import given, when, then
from django.utils import timezone
from datetime import timedelta
import ast

# Factories
from user_management.factories import UserFactory
from projects.factories import ProjectFactory
from design.factories import ResearchQuestionFactory

# Modelos (importar desde __init__.py)
from old.extraction.models import ExtractionPhase, Tag

# Servicios (importar desde servicios separados)
from old.extraction.services.tag_service import TagService
from old.extraction.services.validation_service import ValidationService


# ================================================
# BACKGROUND - Setup común para todos los escenarios
# ================================================

@given("que la fase de extracción está activa")
def step_extraction_phase_active(context):
    """
    Configura un proyecto con fase de extracción activa.

    Este step es parte del Background, se ejecuta antes de cada escenario.
    """
    # 1. Crear usuario Owner
    context.owner = UserFactory(username='test_owner')

    # 2. Crear proyecto
    context.project = ProjectFactory(owner=context.owner)

    # 3. Crear fase de extracción activa
    now = timezone.now()
    start_date = now - timedelta(days=7)  # Empezó hace 1 semana
    end_date = now + timedelta(days=30)  # Termina en 30 días

    context.extraction_phase = ExtractionPhase.objects.create(
        project=context.project,
        is_active=True,
        start_date=start_date,
        end_date=end_date
    )

    # Verificaciones
    assert context.extraction_phase.end_date > now, \
        "El deadline debe estar en el futuro"
    assert context.extraction_phase.is_active is True, \
        "La fase debe estar activa"


# ================================================
# GIVEN - Estado inicial
# ================================================

@given("las Preguntas de Investigación del proyecto son: {pis_list}")
def step_create_research_questions(context, pis_list):
    """
    Crea las preguntas de investigación para el proyecto.

    Args:
        pis_list: String representando una lista Python
                  Ej: '["¿RQ1?", "¿RQ2?"]'

    Ejemplo en feature:
        Given las Preguntas de Investigación del proyecto son: ["¿Cuál?", "¿Cómo?"]
    """
    # Parsear la lista de forma segura
    pi_texts = ast.literal_eval(pis_list)

    # Crear las PIs usando factories
    context.research_questions = [
        ResearchQuestionFactory(project=context.project, text=text)
        for text in pi_texts
    ]

    # Almacenar un dict para lookup fácil
    context.pi_by_text = {
        pi.text: pi for pi in context.research_questions
    }

    # Verificación
    assert len(context.research_questions) == len(pi_texts), \
        f"Esperábamos {len(pi_texts)} PIs, creamos {len(context.research_questions)}"


@given("no existen tags definidos para el proyecto")
def step_no_tags_exist(context):
    """
    Verifica que el proyecto no tenga tags previos.

    Útil para escenarios que requieren un estado limpio.
    """
    tag_count = Tag.objects.filter(
        question__project=context.project
    ).count()

    assert tag_count == 0, \
        f"Se esperaba 0 tags pero existen {tag_count}"


# ================================================
# WHEN - Acciones del usuario
# ================================================

@when("el Owner define los Tags Deductivos y las PIs relacionadas: {tags_definitions}")
def step_owner_defines_tags(context, tags_definitions):
    """
    El Owner crea tags deductivos vinculándolos a PIs.

    Args:
        tags_definitions: String con lista de dicts
                         Ej: '[{"Tag": "IA", "PI_Relacionada": "¿RQ1?"}]'

    Usa: TagService.create_tag()
    """
    # Parsear las definiciones
    definitions = ast.literal_eval(tags_definitions)

    # Almacenar tags creados
    context.created_tags = []

    for definition in definitions:
        tag_name = definition['Tag']
        pi_text = definition['PI_Relacionada']

        # Determinar la PI relacionada
        if pi_text == "<Ninguna>":
            question = None
        else:
            question = context.pi_by_text.get(pi_text)
            if not question:
                raise ValueError(f"PI '{pi_text}' no encontrada en el contexto")

        # ✅ USAR SERVICIO (en vez de create directo)
        tag = TagService.create_tag(
            creator=context.owner,
            project=context.project,
            name=tag_name,
            question=question,
            color='#FFFFFF',
            justification=f"Tag definido para {pi_text or 'ninguna PI'}"
        )

        context.created_tags.append(tag)

    # Verificación
    assert len(context.created_tags) == len(definitions), \
        f"Esperábamos crear {len(definitions)} tags, creamos {len(context.created_tags)}"


@when("un Researcher intenta crear un tag inductivo llamado {tag_name}")
def step_researcher_creates_inductive_tag(context, tag_name):
    """
    Un investigador crea un tag inductivo (emergente del análisis).

    Tags inductivos NO están vinculados a PIs.
    """
    # Crear un researcher si no existe
    if not hasattr(context, 'researcher'):
        context.researcher = UserFactory(username='test_researcher')

    # ✅ USAR SERVICIO
    context.inductive_tag = TagService.create_tag(
        creator=context.researcher,
        project=context.project,
        name=tag_name,
        question=None,  # Los tags inductivos no tienen PI
        color='#FFD700',
        justification="Tag emergente del análisis"
    )


# ================================================
# THEN - Verificaciones
# ================================================

@then("se debe marcar el conjunto de tags obligatorios como: {expected_mandatory_tags}")
def step_verify_mandatory_tags(context, expected_mandatory_tags):
    """
    Verifica que los tags obligatorios sean los esperados.

    Regla de Negocio #10:
    - Tag con PI → is_mandatory = True
    - Tag sin PI → is_mandatory = False
    """
    # Parsear lista esperada
    expected_tags = ast.literal_eval(expected_mandatory_tags)

    # Consultar tags obligatorios REALES en la BD
    actual_mandatory_tags = list(
        Tag.objects.filter(
            question__project=context.project,
            is_mandatory=True
        ).values_list('name', flat=True)
    )

    # Verificación
    assert sorted(actual_mandatory_tags) == sorted(expected_tags), (
        f"Tags obligatorios no coinciden:\n"
        f"  Esperado: {sorted(expected_tags)}\n"
        f"  Obtenido: {sorted(actual_mandatory_tags)}"
    )


@then("se debe determinar la visibilidad de la lista de tags para los Researchers como: {expected_visibility}")
def step_verify_tag_list_visibility(context, expected_visibility):
    """
    Verifica la visibilidad de la lista de tags.

    Regla de Negocio #9:
    - Lista visible si TODAS las PIs tienen al menos un tag
    - Lista oculta si ALGUNA PI no tiene tags

    Args:
        expected_visibility: "Pública" o "No Pública"
    """
    # Convertir string a booleano
    is_expected_public = (expected_visibility == "Pública")

    # ✅ USAR SERVICIO DE VALIDACIÓN
    is_actually_public = ValidationService.is_tag_list_public(
        project=context.project
    )

    # Verificación
    assert is_actually_public == is_expected_public, (
        f"Visibilidad incorrecta:\n"
        f"  Esperada: {expected_visibility}\n"
        f"  Obtenida: {'Pública' if is_actually_public else 'No Pública'}"
    )


@then("el tag {tag_name} debe ser marcado como obligatorio")
def step_verify_tag_is_mandatory(context, tag_name):
    """Verifica que un tag específico sea obligatorio."""
    tag = Tag.objects.get(
        name=tag_name,
        question__project=context.project
    )

    assert tag.is_mandatory is True, \
        f"El tag '{tag_name}' debería ser obligatorio pero no lo es"


@then("el tag {tag_name} debe ser marcado como opcional")
def step_verify_tag_is_optional(context, tag_name):
    """Verifica que un tag específico sea opcional."""
    tag = Tag.objects.get(
        name=tag_name,
        question__project=context.project
    )

    assert tag.is_mandatory is False, \
        f"El tag '{tag_name}' debería ser opcional pero es obligatorio"


@then("el tag {tag_name} debe estar vinculado a la PI {pi_text}")
def step_verify_tag_linked_to_pi(context, tag_name, pi_text):
    """Verifica que un tag esté correctamente vinculado a una PI."""
    tag = Tag.objects.get(
        name=tag_name,
        question__project=context.project
    )

    assert tag.question is not None, \
        f"El tag '{tag_name}' no está vinculado a ninguna PI"

    assert tag.question.text == pi_text, (
        f"El tag '{tag_name}' está vinculado a '{tag.question.text}' "
        f"pero debería estar vinculado a '{pi_text}'"
    )


@then("el tag {tag_name} debe ser de tipo {tag_type}")
def step_verify_tag_type(context, tag_name, tag_type):
    """
    Verifica el tipo de tag (Deductivo o Inductivo).

    Args:
        tag_type: "deductivo" o "inductivo"
    """
    tag = Tag.objects.get(
        name=tag_name,
        question__project=context.project
    )

    expected_type = Tag.TagType.DEDUCTIVE if tag_type.lower() == 'deductivo' else Tag.TagType.INDUCTIVE

    assert tag.type == expected_type, (
        f"El tag '{tag_name}' es de tipo '{tag.get_type_display()}' "
        f"pero debería ser '{tag_type}'"
    )
