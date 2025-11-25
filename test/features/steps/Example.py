from behave import *

from apps.extraction.application.commands.configure_extraction_phase import ConfigureExtractionPhaseCommand
from apps.extraction.domain.repositories.i_project_repository import IProjectRepository
from apps.extraction.domain.repositories.i_extraction_phase_repository import IExtractionPhaseRepository
from apps.extraction.domain.repositories.i_tag_repository import ITagRepository
from apps.extraction.domain.repositories.i_design_repository import IDesignRepository



use_step_matcher("re")


@step("que la fase de extracción está activa")
def step_impl(context):
    extractionPhase = ConfigureExtractionPhaseCommand(1,1,"Single")
    context.result = context.container.create_extraction_handler(extractionPhase)


@step("las Preguntas de Investigación del proyecto son: (?P<PIs_Existentes>.+)")
def step_impl(context, PIs_Existentes):
    raise NotImplementedError(u'STEP: Dadas las Preguntas de Investigación del proyecto son: <PIs_Existentes>')


@step("el Owner define los Tags Deductivos y las PIs relacionadas: (?P<Tags_Definidos>.+)")
def step_impl(context, Tags_Definidos):
    raise NotImplementedError(
        u'STEP: Cuando el Owner define los Tags Deductivos y las PIs relacionadas: <Tags_Definidos>')


@step("se debe marcar el conjunto de tags obligatorios como: (?P<Tags_Obligatorios_Esperados>.+)")
def step_impl(context, Tags_Obligatorios_Esperados):
    raise NotImplementedError(
        u'STEP: Entonces se debe marcar el conjunto de tags obligatorios como: <Tags_Obligatorios_Esperados>')


@step("se debe determinar la visibilidad de la lista de tags para los Researchers como: (?P<Visibilidad_Esperada>.+)")
def step_impl(context, Visibilidad_Esperada):
    raise NotImplementedError(
        u'STEP: Y se debe determinar la visibilidad de la lista de tags para los Researchers como: <Visibilidad_Esperada>')


@step("una lista de tags obligatorios para la extracción: (?P<Tags_Obligatorios>.+)")
def step_impl(context, Tags_Obligatorios):
    raise NotImplementedError(u'STEP: Dada una lista de tags obligatorios para la extracción: <Tags_Obligatorios>')


@step("se han registrado las extracciones para los siguientes tags: (?P<Tags_Extraidos>.+)")
def step_impl(context, Tags_Extraidos):
    raise NotImplementedError(u'STEP: Y se han registrado las extracciones para los siguientes tags: <Tags_Extraidos>')


@step('el investigador intenta marcar el paper como "Completo"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Cuando el investigador intenta marcar el paper como "Completo"')


@step('el estado del paper debe ser "(?P<Estado_Esperado>.+)"')
def step_impl(context, Estado_Esperado):
    raise NotImplementedError(u'STEP: Entonces el estado del paper debe ser "<Estado_Esperado>"')


@step("se debe notificar al investigador sobre los tags pendientes: (?P<Tags_Pendientes_Esperados>.+)")
def step_impl(context, Tags_Pendientes_Esperados):
    raise NotImplementedError(
        u'STEP: Y se debe notificar al investigador sobre los tags pendientes: <Tags_Pendientes_Esperados>')