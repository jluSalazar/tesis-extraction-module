# 🎯 Objetivo
Crear la base del **primer MVP** de la aplicación Django para la **fase de extracción** de una Revisión Sistemática de Literatura (RSL).  
El enfoque es modular, escalable y compatible con **herencia de modelos**, **fake services**, y **estructuración por tipo de recurso (models/, views/, templates/, repositories/)**.  
El frontend utilizará **DaisyUI** para los templates.

---

# ⚙️ Especificaciones Generales

- Framework: **Django 5.x**
- Base de datos: **PostgreSQL**
- Lenguaje: **Python 3.11+**
- Estilo de carpetas: agrupación por tipo (`models/`, `views/`, `templates/`, `repositories/`)
- Fake Services: para entidades externas (papers y preguntas de investigación)
- Usuarios manejados desde otra app (`users`):
  - `Owner` → dueño de la investigación
  - `Researcher` → asistente de investigación

---

# 🧩 Modelos Principales

## 1. ResearchProject *(🔹 Fake Service: módulo de proyecto)*
Representa el proyecto de investigación o revisión sistemática.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| `title` | CharField | Título del proyecto o revisión |
| `description` | TextField | Descripción general del proyecto |
| `owner` | ForeignKey(User) | Usuario que define el protocolo |
| `created_at` | DateTimeField | Fecha de creación |
| `status` | CharField (`Draft`, `ExtractionActive`, `Closed`) | Estado general del proyecto |

---

## 1. Extraction
**Configuración general de la fase de extracción.**

| Campo | Tipo | Descripción |
|--------|------|-------------|
| `start_date` | DateTimeField | Fecha de inicio de la fase |
| `end_date` | DateTimeField | Fecha límite de extracción |
| `is_active` | BooleanField | Controla si la fase está activa |
| `double_extraction` | BooleanField | Si se requiere doble revisión por paper |
| `auto_close` | BooleanField | Cierra automáticamente al alcanzar el deadline |
| `created_at` | DateTimeField | Fecha de creación |


---

## 2. Paper *(🔹 Fake Service: módulo externo de carga / metadata)*
Representa los documentos analizados.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| `title` | CharField | Título |
| `authors` | CharField | Autores |
| `year` | IntegerField | Año de publicación |
| `metadata` | JSONField | Datos extendidos |
| `fulltext` | TextField | Texto completo o referencia |
| `status` | CharField (`Pending`, `InProgress`, `Done`) | Estado de extracción |
| `uploaded_by` | ForeignKey(User) | Usuario que cargó el paper |
| `created_at` | DateTimeField | Fecha de creación |

---

## 3. Quote
Fragmentos o porciones de texto extraídos de los papers.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| `text_portion` | TextField | Fragmento textual |
| `paper` | ForeignKey(Paper) | Paper del que proviene |
| `location` | CharField | Ubicación (página, párrafo, etc.) |
| `comment` | TextField | Interpretación o nota del investigador |
| `tags` | ManyToManyField(Tag) | Códigos aplicados |
| `researcher` | ForeignKey(User) | Investigador que realizó la extracción |
| `created_at` | DateTimeField | Fecha de registro |
| `validated` | BooleanField | Indica si fue revisada |
| `version` | IntegerField | Control de versiones |

---

## 4. Comment
Comentarios o revisiones sobre una `Quote`.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| `quote` | ForeignKey(Quote) | Cita comentada |
| `user` | ForeignKey(User) | Revisor o investigador |
| `text` | TextField | Comentario |
| `created_at` | DateTimeField | Fecha |
| `is_review` | BooleanField | Si es parte de doble revisión |

---

## 5. Tag
Interfaz base para todos los tipos de tags (códigos).

| Campo | Tipo | Descripción |
|--------|------|-------------|
| `name` | CharField | Nombre del tag |
| `color` | CharField | Color visual (hex o clase DaisyUI) |
| `justification` | TextField (opcional) | Justificación o descripción conceptual |
| `created_at` | DateTimeField | Fecha de creación |
| `created_by` | ForeignKey(User) | Autor del tag |
| `question` | ForeignKey(ResearchQuestion, null=True, blank=True) | Pregunta asociada (si aplica) |
| `type` | CharField (`deductive`, `inductive`) | Tipo de tag |
| `is_mandatory` | BooleanField | Si es requerido para completar la extracción |
| `is_public` | BooleanField | Si es visible para los investigadores |


## 6. ResearchQuestion *(🔹 Fake Service: módulo de diseño del protocolo)*
Modelo externo consumido vía API.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| `id` | IntegerField | ID externo |
| `text` | TextField | Contenido de la pregunta |
| `project_id` | IntegerField | Proyecto asociado |

---

## 7. ErrorHandler
Notificaciones automáticas cuando faltan extracciones obligatorias.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| `paper` | ForeignKey(Paper) | Paper afectado |
| `user` | ForeignKey(User) | Usuario notificado |
| `missing_tags` | JSONField | Tags faltantes |
| `message` | TextField | Mensaje generado |
| `sent_at` | DateTimeField | Fecha del envío |

---

# 🔗 Relaciones Principales

```text
Extraction
 ├── Paper (fake service)
 │    └── Quote
 │         ├── Tag
 │         │    ├── DeductiveTag
 │         │    └── InductiveTag
 │         └── Comment
 ├── ResearchQuestion (fake service)
 └── ErrorHandler
```

---

# 📦 Estructura de Carpetas Django

```text
extraction_app/
│
├── models/
│   ├── __init__.py
│   ├── extraction.py
│   ├── quote.py
│   ├── comment.py
│   ├── tag_base.py
│   ├── tag_deductive.py
│   ├── tag_inductive.py
│   ├── paper_fake_service.py
│   └── research_question_fake_service.py
│
├── repositories/
│   ├── __init__.py
│   ├── quote_repository.py
│   ├── tag_repository.py
│   ├── extraction_repository.py
│   └── paper_repository.py
│
├── views/
│   ├── __init__.py
│   ├── extraction_views.py
│   ├── quote_views.py
│   ├── tag_views.py
│   └── dashboard_views.py
│
├── templates/
│   ├── base.html
│   ├── extraction/
│   │   ├── index.html
│   │   ├── form.html
│   │   └── dashboard.html
│   ├── quotes/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── edit.html
│   └── tags/
│       ├── list.html
│       ├── edit.html
│       └── create.html
│
├── static/
│   ├── css/
│   │   └── daisyui_custom.css
│   └── js/
│       └── extraction.js
│
├── urls.py
├── admin.py
└── apps.py
```

---

# 🧠Reglas de Negocio
1. La extracción solo puede realizarse cuando la fase está activa.
2. Cada tag debe tener una definición formal en el diccionario de tags.
3. Todo tag debe estar asociado a una categoría principal o subcategoría temática.
4. Si un texto coincide con más de un patrón semántico, se permiten múltiples tags.
5. Cada quote debe poder rastrearse hasta su fuente (documento, párrafo, oración).
6. Cada quote debe registrar quién extrajo y cuándo.
7. Solo el Owner del proyecto puede definir o aprobar los tags deductivos.
8. Cada tag deductivo debe estar vinculado a al menos una pregunta de investigación (PI) para considerarse válido.
9. Si ningún tag está vinculado a una PI, la lista de tags no será visible para los investigadores.
10. Los tags vinculados a preguntas de investigación deben marcarse como “obligatorios” para las extracciones.
11. Los tags sin relación con ninguna PI permanecen como “opcionales”.
12. Un paper solo puede marcarse como “Completo” si todas las extracciones obligatorias han sido registradas.
13. Si faltan tags obligatorios, el estado se mantiene en “In progress”.
14. Al alcanzar la fecha límite (deadline), el sistema cambia automáticamente la fase de extracción a “cerrada”.
15. Las extracciones en curso al cierre deben conservar su último estado.
16. Cualquier intento de extracción o edición en fase cerrada genera un mensaje de error de tipo “Fase no activa”.
17. Todo fragmento de texto extraído debe tener al menos un tag asignado.


---

# 💡 Futuras Extensiones (no implementar ahora)

- Sugerencias automáticas de códigos mediante IA.  
- Clasificación inductiva de fragmentos pendientes.  
- Normalización automática de tags (`AI`, `ai`, `A.I.` → `ai`).  
- Campo `origin` (`manual` / `auto` / `revisado`) para trazabilidad.  
- Actualización retroactiva de tags en las quotes afectadas.

---

✅ Este prompt ya está optimizado para que una IA (ChatGPT, Copilot, o un generador de scaffolds Django) pueda:
1. Crear automáticamente el proyecto y la app `extraction_app`.
2. Generar las clases Django ORM.
3. Construir la estructura modular de carpetas.
4. Dejar placeholders para los fake services y templates DaisyUI.

---
