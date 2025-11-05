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