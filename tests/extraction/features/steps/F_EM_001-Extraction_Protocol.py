from behave import *

use_step_matcher("re")


@step("que la fase de extracción está activa")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Dado que la fase de extracción está activa')


@step("las Preguntas de Investigación del proyecto son: (?P<PIs_Existentes>.+)")
def step_impl(context, PIs_Existentes):
    """
    :type context: behave.runner.Context
    :type PIs_Existentes: str
    """
    raise NotImplementedError(u'STEP: Dadas las Preguntas de Investigación del proyecto son: <PIs_Existentes>')


@step("el Owner define los Tags Deductivos y las PIs relacionadas: (?P<Tags_Definidos>.+)")
def step_impl(context, Tags_Definidos):
    """
    :type context: behave.runner.Context
    :type Tags_Definidos: str
    """
    raise NotImplementedError(
        u'STEP: Cuando el Owner define los Tags Deductivos y las PIs relacionadas: <Tags_Definidos>')


@step("se debe marcar el conjunto de tags obligatorios como: (?P<Tags_Obligatorios_Esperados>.+)")
def step_impl(context, Tags_Obligatorios_Esperados):
    """
    :type context: behave.runner.Context
    :type Tags_Obligatorios_Esperados: str
    """
    raise NotImplementedError(
        u'STEP: Entonces se debe marcar el conjunto de tags obligatorios como: <Tags_Obligatorios_Esperados>')


@step("se debe determinar la visibilidad de la lista de tags para los Researchers como: (?P<Visibilidad_Esperada>.+)")
def step_impl(context, Visibilidad_Esperada):
    """
    :type context: behave.runner.Context
    :type Visibilidad_Esperada: str
    """
    raise NotImplementedError(
        u'STEP: Y se debe determinar la visibilidad de la lista de tags para los Researchers como: <Visibilidad_Esperada>')


@step("una lista de tags obligatorios para la extracción: (?P<Tags_Obligatorios>.+)")
def step_impl(context, Tags_Obligatorios):
    """
    :type context: behave.runner.Context
    :type Tags_Obligatorios: str
    """
    raise NotImplementedError(u'STEP: Dada una lista de tags obligatorios para la extracción: <Tags_Obligatorios>')


@step("se han registrado las extracciones para los siguientes tags: (?P<Tags_Extraidos>.+)")
def step_impl(context, Tags_Extraidos):
    """
    :type context: behave.runner.Context
    :type Tags_Extraidos: str
    """
    raise NotImplementedError(u'STEP: Y se han registrado las extracciones para los siguientes tags: <Tags_Extraidos>')


@step('el investigador intenta marcar el paper como "Completo"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Cuando el investigador intenta marcar el paper como "Completo"')


@step('el estado del paper debe ser "(?P<Estado_Esperado>.+)"')
def step_impl(context, Estado_Esperado):
    """
    :type context: behave.runner.Context
    :type Estado_Esperado: str
    """
    raise NotImplementedError(u'STEP: Entonces el estado del paper debe ser "<Estado_Esperado>"')


@step("se debe notificar al investigador sobre los tags pendientes: (?P<Tags_Pendientes_Esperados>.+)")
def step_impl(context, Tags_Pendientes_Esperados):
    """
    :type context: behave.runner.Context
    :type Tags_Pendientes_Esperados: str
    """
    raise NotImplementedError(
        u'STEP: Y se debe notificar al investigador sobre los tags pendientes: <Tags_Pendientes_Esperados>')