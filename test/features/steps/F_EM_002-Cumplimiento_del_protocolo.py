from behave import *

use_step_matcher("re")


@step("la fase de extracción está activa")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Dado la fase de extracción está activa')


@step("una lista de tags obligatorios para la extracción:")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Dada una lista de tags obligatorios para la extracción:
                              | Eficiencia |
                              | Costos |
                              | Tiempo |
                              | Impacto
    Ambiental | ')


@step("se han registrado las extracciones relacionadas con los siguientes tags:")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Y se han registrado las extracciones relacionadas con los siguientes tags:
                              | Tiempo |
                              | Impacto
    Ambiental | ')


@step('el investigador cambia el estado del paper a "Completo"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Cuando el investigador cambia el estado del paper a "Completo"')


@step('el estado del paper será "Pendiente"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Entonces el estado del paper será "Pendiente"')


@step("se notificará al investigador que aún le falta completar las extracciones requeridas para los tags:")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Y se notificará al investigador que aún le falta completar las extracciones requeridas para los tags:
        | Eficiencia |
        | Costos | ')


@step("que la fase de extraccion no está activa")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Dado que la fase de extraccion no está activa')


@step("el deadline de la fase de extraccion se haya alcanzado")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Cuando el deadline de la fase de extraccion se haya alcanzado')


@step("la fase de extracción no permitirá mas cambios por los investigadores")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Entonces la fase de extracción no permitirá mas cambios por los investigadores')