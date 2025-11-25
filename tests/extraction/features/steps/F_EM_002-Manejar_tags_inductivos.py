from behave import *

use_step_matcher("re")


@step('que el Investigador "Juan" está extrayendo datos de un estudio')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Dado que el Investigador "Juan" está extrayendo datos de un estudio')


@step('"Juan" crea un nuevo tag inductivo llamado "Resistencia al cambio"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Cuando "Juan" crea un nuevo tag inductivo llamado "Resistencia al cambio"')


@step("se debe registrar el tag con:")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Entonces se debe registrar el tag con:
                              | Nombre | Propietario | Estado | Visibilidad |
                              | Resistencia
    al
    cambio | Juan | Pendiente
    de
    Aprobación | Privada | ')


@step('el tag "Resistencia al cambio" debe estar disponible para ser usado por "Juan" en otros papers')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Y el tag "Resistencia al cambio" debe estar disponible para ser usado por "Juan" en otros papers')


@step('el tag "Resistencia al cambio" NO debe aparecer en la lista de tags del Investigador "Ana"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Pero el tag "Resistencia al cambio" NO debe aparecer en la lista de tags del Investigador "Ana"')


@step('que existe un tag "(?P<Nombre_Tag>.+)" propuesto por "Juan" con estado "Pendiente de Aprobación"')
def step_impl(context, Nombre_Tag):
    """
    :type context: behave.runner.Context
    :type Nombre_Tag: str
    """
    raise NotImplementedError(
        u'STEP: Dado que existe un tag "<Nombre_Tag>" propuesto por "Juan" con estado "Pendiente de Aprobación"')


@step("el Owner decide (?P<Accion_Owner>.+) la propuesta")
def step_impl(context, Accion_Owner):
    """
    :type context: behave.runner.Context
    :type Accion_Owner: str
    """
    raise NotImplementedError(u'STEP: Cuando el Owner decide <Accion_Owner> la propuesta')


@step('el estado del tag cambia a "(?P<Estado_Final>.+)"')
def step_impl(context, Estado_Final):
    """
    :type context: behave.runner.Context
    :type Estado_Final: str
    """
    raise NotImplementedError(u'STEP: Entonces el estado del tag cambia a "<Estado_Final>"')


@step('la visibilidad para el resto del equipo \(ej\. "Ana"\) pasa a ser "(?P<Visibilidad_Equipo>.+)"')
def step_impl(context, Visibilidad_Equipo):
    """
    :type context: behave.runner.Context
    :type Visibilidad_Equipo: str
    """
    raise NotImplementedError(
        u'STEP: Y la visibilidad para el resto del equipo (ej. "Ana") pasa a ser "<Visibilidad_Equipo>"')


@step("la existencia de los siguientes tags propuestos pendientes:")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Dada la existencia de los siguientes tags propuestos pendientes:
                              | Nombre_Tag | Propietario |
                              | Costo
    oculto | Juan |
    | Costos
    oc. | Ana | ')


@step('el Owner aprueba "Costo oculto" y lo marca como equivalente a "Costos oc\."')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Cuando el Owner aprueba "Costo oculto" y lo marca como equivalente a "Costos oc."')


@step('ambos tags se fusionan en un único tag global "Costo oculto"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Entonces ambos tags se fusionan en un único tag global "Costo oculto"')


@step('las extracciones que "Ana" hizo con "Costos oc\." ahora deben estar asociadas al tag aprobado "Costo oculto"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Y las extracciones que "Ana" hizo con "Costos oc." ahora deben estar asociadas al tag aprobado "Costo oculto"')