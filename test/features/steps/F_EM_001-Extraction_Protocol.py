from behave import *
from django.contrib.auth import get_user_model
import ast # Usamos 'ast' para parsear de forma segura los strings del feature
from django.utils import timezone
from datetime import timedelta

# Importamos las factories de nuestros módulos
from user_management.factories import UserFactory
from projects.factories import ProjectFactory
from design.factories import ResearchQuestionFactory
from extraction.models import ExtractionPhase, Tag
from extraction import services # Importamos nuestra lógica de negocio

use_step_matcher("re")


# (Background) Configura el mundo base
@step("que la fase de extracción está activa")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.owner = UserFactory(username='test_owner')
    context.project = ProjectFactory(owner=context.owner)

    # Para que una fase esté "activa", debe tener fechas válidas.
    now = timezone.now()
    start_date = now - timedelta(days=7)  # Empezó hace 1 semana
    end_date = now + timedelta(days=30)  # Termina en 30 días (el deadline)

    context.extraction_config = ExtractionPhase.objects.create(
        project=context.project,
        is_active=True,
        start_date=start_date,
        end_date=end_date
    )

    assert context.extraction_config.end_date > now, "El deadline (end_date) de la fase de extracción debe estar en el futuro."
    assert context.extraction_config.is_active == True


# (Given) Parseamos la lista de strings de PIs
@step("las Preguntas de Investigación del proyecto son: (?P<PIs_Existentes>.+)")
def step_impl(context, PIs_Existentes):
    """
    :type context: behave.runner.Context
    :type PIs_Existentes: str
    """
    pi_texts = ast.literal_eval(PIs_Existentes)
    context.pis = []
    for text in pi_texts:
        pi = ResearchQuestionFactory(project=context.project, text=text)
        context.pis.append(pi)

    assert len(context.pis) == len(pi_texts)


# (When) Ejecutamos el Caso de Uso
@step("el Owner define los Tags Deductivos y las PIs relacionadas: (?P<Tags_Definidos>.+)")
def step_impl(context, Tags_Definidos):
    """
    :type context: behave.runner.Context
    :type Tags_Definidos: str
    """
    tags_definitions = ast.literal_eval(Tags_Definidos)
    context.created_tags = []
    print(">> Tipo:", type(Tags_Definidos))
    print(">> Valor:", repr(Tags_Definidos))

    for definition in tags_definitions:
        tag_name = definition['Tag']
        pi_text = definition['PI_Relacionada']

        if pi_text == "<Ninguna>":
            pi_text = None

        # Llamamos al servicio que encapsula la lógica de negocio
        tag = services.create_tag_with_pi(
            creator=context.owner,
            project=context.project,
            tag_name=tag_name,
            pi_text=pi_text
        )
        context.created_tags.append(tag)


# (Then) Verificamos si es obligatorio (is_mandatory)
@step("se debe marcar el conjunto de tags obligatorios como: (?P<Tags_Obligatorios_Esperados>.+)")
def step_impl(context, Tags_Obligatorios_Esperados):
    """
    :type context: behave.runner.Context
    :type Tags_Obligatorios_Esperados: str
    """
    expected_tags_list = ast.literal_eval(Tags_Obligatorios_Esperados)

    # Consultamos la base de datos para ver el resultado real
    actual_mandatory_tags = list(
        Tag.objects.filter(
            question__project=context.project,
            is_mandatory=True
        ).values_list('name', flat=True)
    )

    assert sorted(actual_mandatory_tags) == sorted(expected_tags_list), (
        f"Los tags obligatorios no coinciden.\n"
        f"Esperado: {sorted(expected_tags_list)}\n"
        f"Obtenido: {sorted(actual_mandatory_tags)}"
    )


    # (Then) Verificamos la visibilidad para los researchers
@step("se debe determinar la visibilidad de la lista de tags para los Researchers como: (?P<Visibilidad_Esperada>.+)")
def step_impl(context, Visibilidad_Esperada):
    """
    :type context: behave.runner.Context
    :type Visibilidad_Esperada: str
    """

    # Convertimos el string "Pública" / "No Pública" a booleano
    expected_visibility = (Visibilidad_Esperada == "Pública")

    # Llamamos al servicio que encapsula esta lógica de consulta
    actual_visibility = services.is_tag_list_public(project=context.project)

    assert actual_visibility == expected_visibility, (
        f"La visibilidad esperada era '{Visibilidad_Esperada}', "
        f"pero el resultado fue {'Pública' if actual_visibility else 'No Pública'}."
    )