# Created by jona at 27/10/25
#language: es
Característica: Refinamiento del protocolo de extracción
  Para garantizar que la extracción cubre todos los aspectos críticos del protocolo de extracción,
  Como Dueño de la investigación,
  Quiero definir y aprobar el conjunto de tags que serán utilizados obligatoriamente.

  Antecedentes:
    Dado que la fase de extracción está activa

  Esquema del escenario: Extracción obligatoria de Tags Deductivos acorde a su relación con Preguntas de Investigación
  Dadas las Preguntas de Investigación del proyecto son: <PIs_Existentes>
  Cuando el Owner define los Tags Deductivos y las PIs relacionadas: <Tags_Definidos>
  Entonces se debe marcar el conjunto de tags obligatorios como: <Tags_Obligatorios_Esperados>
  Y se debe determinar la visibilidad de la lista de tags para los Researchers como: <Visibilidad_Esperada>

  Ejemplos:
    | PIs_Existentes                                                                                                                                                          | Tags_Definidos                                                                                                                                                                                                                                                                                                             | Tags_Obligatorios_Esperados | Visibilidad_Esperada |
    | "Cómo afectan las nuevas tecnologías a la eficiencia operativa de las empresas?", "Cuáles son los costos asociados con la implementación de tecnologías emergentes?"    | [ {Tag: Eficiencia, PI_Relacionada: <Ninguna>}, {Tag: Costos, PI_Relacionada: <Ninguna>}, {Tag: Tiempo, PI_Relacionada: <Ninguna>}, {Tag: Impacto Ambiental, PI_Relacionada: <Ninguna>} ]                                                                                                                                  | []                          | No Pública           |
    | "Cómo afectan las nuevas tecnologías a la eficiencia operativa de las empresas?", "Cuáles son los costos asociados con la implementación de tecnologías emergentes?"    | [ {Tag: Eficiencia, PI_Relacionada: "Cómo afecta la eficiencia operativa en la reducción de costos?"}, {Tag: Costos, PI_Relacionada: "Cuáles son los costos asociados con la implementación de tecnologías emergentes?"}, {Tag: Tiempo, PI_Relacionada: <Ninguna>}, {Tag: Impacto Ambiental, PI_Relacionada: <Ninguna>} ]  | ["Eficiencia", "Costos"]    | Pública              |





    """
    Escenario: Trazabilidad de tags deductivos
    Dadas las preguntas de investigacion del proyecto
      | ¿Cómo afectan las nuevas tecnologías a la eficiencia operativa de las empresas?     |
      | ¿Cuáles son los costos asociados con la implementación de tecnologías emergentes?   |
    Cuando el Owner define la lista de tags deductivos del proyecto
      | Tag              |  Pregunta de investigación relacionada |
      | Eficiencia       |  |
      | Costos           |  |
      | Tiempo           |  |
      | Impacto Ambiental|  |
    Y ninguna pregunta está relacionada con al menos un tag
    Entonces no se hará pública la lista de tags para los investigadores

  Escenario:
    Dadas las preguntas de investigacion del proyecto
      | ¿Cómo afectan las nuevas tecnologías a la eficiencia operativa de las empresas?     |
      | ¿Cuáles son los costos asociados con la implementación de tecnologías emergentes?   |
    Cuando el Owner define la lista de tags deductivos del proyecto:
      | Tag              |  Pregunta de investigación relacionada                             |
      | Eficiencia       | ¿Cómo afecta la eficiencia operativa en la reducción de costos?    |
      | Costos           | ¿Cuáles son los costos asociados con la implementación de tecnologías emergentes?   |
      | Tiempo           |  |
      | Impacto Ambiental | |
    Entonces los tags "Eficiencia" y "Costos" deben ser marcados automáticamente como obligatorios para las extracciones
    """