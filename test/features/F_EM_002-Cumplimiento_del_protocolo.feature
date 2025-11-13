# Created by jona at 28/10/25
#language: es
Característica: Validación de la Completitud de la Extracción de Tags
  Para asegurar que toda la información relevante ha sido extraída según el protocolo,
  Como Dueño de la investigación,
  Quiero que el sistema valide que todas las extracciones obligatorias estén completas antes de finalizar el proceso de un paper.

  Antecedentes:
    Dado la fase de extracción está activa

  Esquema del escenario: Validar que un paper no puede marcarse como "Completo" si faltan extracciones obligatorias
    Dada una lista de tags obligatorios para la extracción: <Tags_Obligatorios>
    Y se han registrado las extracciones para los siguientes tags: <Tags_Extraidos>
    Cuando el investigador intenta marcar el paper como "Completo"
    Entonces el estado del paper debe ser "<Estado_Esperado>"
    Y se debe notificar al investigador sobre los tags pendientes: <Tags_Pendientes_Esperados>

  Ejemplos:
    | Tags_Obligatorios                                     | Tags_Extraidos                  | Estado_Esperado | Tags_Pendientes_Esperados |
    | ["Eficiencia", "Costos", "Tiempo", "Impacto Ambiental"] | ["Tiempo", "Impacto Ambiental"] | "Pendiente"     | ["Eficiencia", "Costos"]  |
    | ["Eficiencia", "Costos", "Tiempo"]                      | ["Eficiencia", "Costos", "Tiempo"] | "Completo"      | []                        |