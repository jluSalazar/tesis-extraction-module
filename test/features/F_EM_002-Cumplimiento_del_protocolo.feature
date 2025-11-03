# Created by jona at 28/10/25
#language: es
Característica: # Enter feature name here
  # Enter feature description here
  Antecedentes:
    Dado la fase de extracción está activa

  Escenario:
    Dada una lista de tags obligatorios para la extracción:
      | Eficiencia       |
      | Costos           |
      | Tiempo           |
      | Impacto Ambiental |
    Y se han registrado las extracciones relacionadas con los siguientes tags:
      | Tiempo           |
      | Impacto Ambiental |
    Cuando el investigador cambia el estado del paper a "Completo"
    Entonces el estado del paper será "Pendiente"
    Y se notificará al investigador que aún le falta completar las extracciones requeridas para los tags:
      | Eficiencia       |
      | Costos           |

    Escenario: Researcher trata de realizar una extraccion cuando la fase de extraccion no está activa
      Dado que la fase de extraccion no está activa
      Cuando el deadline de la fase de extraccion se haya alcanzado
      Entonces la fase de extracción no permitirá mas cambios por los investigadores

