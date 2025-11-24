# Scaffolding App Extraction - Estructura Mejorada

## Estructura Completa con Comentarios

```
apps/extraction/
├── __init__.py
├── apps.py                          # Configuración de la app Django
├── admin.py                         # Admin de Django (solo para debugging)
├── urls.py                          # URLs principales de la app
├── README.md                        # Documentación: qué hace esta app y cómo usarla
│
├── api/                             # 📡 CAPA DE PRESENTACIÓN
│   ├── serializers.py               # DTOs de entrada/salida para API REST
│   ├── views.py                     # ViewSets/APIViews - maneja HTTP requests
│   ├── filters.py                   # Filtros personalizados para queries
│   └── urls.py                      # URLs específicas de la API
│
├── application/                     # 🎯 CAPA DE APLICACIÓN - Casos de Uso
│   ├── __init__.py                  # Orquesta el flujo de negocio
│   │
│   ├── commands/                    # Operaciones que MODIFICAN estado (CQS pattern)
│   │   ├── __init__.py
│   │   ├── create_extraction.py     # Comando: crear nueva extracción
│   │   ├── update_extraction.py     # Comando: actualizar extracción
│   │   ├── submit_for_review.py     # Comando: enviar a revisión
│   │   ├── approve_extraction.py    # Comando: aprobar extracción
│   │   └── reject_extraction.py     # Comando: rechazar extracción
│   │
│   ├── queries/                     # Operaciones de LECTURA (CQS pattern)
│   │   ├── __init__.py
│   │   ├── get_extraction_by_id.py  # Query: obtener por ID
│   │   ├── list_extractions.py      # Query: listar con filtros
│   │   ├── get_by_study.py          # Query: extracciones de un estudio
│   │   └── get_statistics.py        # Query: estadísticas agregadas
│   │
│   └── services/                    # Servicios de aplicación (coordinan casos de uso)
│       ├── __init__.py
│       ├── extraction_orchestrator.py    # Orquesta flujo completo de extracción
│       └── extraction_validator_service.py # Coordina validación completa
│
├── domain/                          # 💎 CAPA DE DOMINIO - Lógica de Negocio Pura
│   ├── __init__.py                  # NO depende de Django, frameworks, ni DB
│   │
│   ├── entities/                    # Entidades del dominio (tienen identidad)
│   │   ├── __init__.py
│   │   ├── extraction.py            # Entidad: Extracción (con comportamiento)
│   │   ├── extraction_field.py      # Entidad: Campo extraído
│   │   ├── extraction_template.py   # Entidad: Plantilla de extracción
│   │   └── quality_assessment.py    # Entidad: Evaluación de calidad
│   │
│   ├── value_objects/               # Value Objects (sin identidad, inmutables)
│   │   ├── __init__.py
│   │   ├── extraction_status.py     # VO: Estado de extracción (enum)
│   │   ├── field_type.py            # VO: Tipo de campo (text, number, etc)
│   │   ├── quality_score.py         # VO: Score de calidad (0-100)
│   │   └── extraction_metadata.py   # VO: Metadatos de extracción
│   │
│   ├── events/                      # Domain Events (para comunicación desacoplada)
│   │   ├── __init__.py
│   │   ├── extraction_created.py    # Evento: extracción creada
│   │   ├── extraction_completed.py  # Evento: extracción completada
│   │   ├── extraction_approved.py   # Evento: extracción aprobada
│   │   └── validation_failed.py     # Evento: validación falló
│   │
│   ├── exceptions/                  # Excepciones del dominio
│   │   ├── __init__.py
│   │   ├── extraction_exceptions.py # Excepciones relacionadas a extracción
│   │   └── validation_exceptions.py # Excepciones de validación
│   │
│   ├── repositories/                # 🔌 INTERFACES de repositorios (contratos)
│   │   ├── __init__.py              # Implementaciones están en infrastructure/
│   │   ├── i_extraction_repository.py    # Interface: repo de extracciones
│   │   ├── i_template_repository.py      # Interface: repo de templates
│   │   └── i_quality_repository.py       # Interface: repo de calidad
│   │
│   └── services/                    # Servicios del dominio (lógica de negocio)
│       ├── __init__.py
│       ├── extraction_validator.py  # Servicio: valida reglas de negocio
│       ├── quality_calculator.py    # Servicio: calcula métricas de calidad
│       ├── conflict_resolver.py     # Servicio: resuelve conflictos entre extractores
│       └── data_normalizer.py       # Servicio: normaliza datos extraídos
│
├── infrastructure/                  # 🔧 CAPA DE INFRAESTRUCTURA - Detalles Técnicos
│   ├── __init__.py                  # Implementaciones concretas de interfaces
│   │
│   ├── models.py                    # Modelos Django ORM (mapeo a DB)
│   │
│   ├── repositories/                # Implementaciones de repositorios
│   │   ├── __init__.py
│   │   ├── django_extraction_repository.py   # Implementa i_extraction_repository
│   │   ├── django_template_repository.py     # Implementa i_template_repository
│   │   └── django_quality_repository.py      # Implementa i_quality_repository
│   │
│   ├── adapters/                    # Adaptadores a sistemas externos
│   │   ├── __init__.py
│   │   │
│   │   ├── outbound/                # Llamadas SALIENTES a servicios externos
│   │   │   ├── __init__.py
│   │   │   ├── ai_extraction_adapter.py      # Adapter: servicio IA para extracción
│   │   │   ├── ocr_adapter.py                # Adapter: servicio OCR
│   │   │   └── storage_adapter.py            # Adapter: almacenamiento de archivos
│   │   │
│   │   └── inbound/                 # Adaptadores ENTRANTES (parsers, etc)
│   │       ├── __init__.py
│   │       ├── pdf_parser.py        # Parser: extrae datos de PDFs
│   │       ├── excel_parser.py      # Parser: extrae datos de Excel
│   │       └── csv_parser.py        # Parser: extrae datos de CSV
│   │
│   └── tasks/                       # Tareas asíncronas (Celery)
│       ├── __init__.py
│       ├── extraction_tasks.py      # Tasks: procesamiento asíncrono
│       └── validation_tasks.py      # Tasks: validación en background
│
├── interfaces/                      # 🌐 INTERFACE PÚBLICA (para otras apps)
│   ├── __init__.py                  # ÚNICA forma de comunicarse con esta app
│   │
│   ├── dtos/                        # Data Transfer Objects (contratos de datos)
│   │   ├── __init__.py
│   │   ├── extraction_dto.py        # DTO: representa una extracción
│   │   ├── extraction_result_dto.py # DTO: resultado de operación
│   │   ├── validation_result_dto.py # DTO: resultado de validación
│   │   └── statistics_dto.py        # DTO: estadísticas agregadas
│   │
│   └── services/                    # Interfaces de servicios públicos
│       ├── __init__.py
│       └── i_extraction_service.py  # Interface pública del servicio
│                                    # Otras apps solo importan ESTO
│
├── migrations/                      # Migraciones de Django
│   └── __init__.py
│
├── templates/                       # Templates HTML (si hay UI web)
│   └── extraction/
│       ├── extraction_list.html     # Lista de extracciones
│       ├── extraction_detail.html   # Detalle de extracción
│       └── extraction_form.html     # Formulario de extracción
│
└── tests/                           # 🧪 TESTS organizados por capa
    ├── __init__.py
    │
    ├── unit/                        # Tests unitarios (sin DB, sin red)
    │   ├── __init__.py
    │   │
    │   ├── domain/                  # Tests de lógica de negocio pura
    │   │   ├── __init__.py
    │   │   ├── test_extraction_entity.py      # Test: comportamiento de Extraction
    │   │   ├── test_value_objects.py          # Test: value objects
    │   │   ├── test_extraction_validator.py   # Test: validaciones de negocio
    │   │   └── test_quality_calculator.py     # Test: cálculo de calidad
    │   │
    │   └── application/             # Tests de casos de uso
    │       ├── __init__.py
    │       ├── test_commands.py     # Test: comandos funcionan correctamente
    │       ├── test_queries.py      # Test: queries retornan datos correctos
    │       └── test_orchestrator.py # Test: orquestación de flujos
    │
    ├── integration/                 # Tests de integración (con DB, con servicios)
    │   ├── __init__.py
    │   ├── test_repositories.py     # Test: repositorios con DB real
    │   ├── test_api_endpoints.py    # Test: endpoints de API
    │   └── test_extraction_workflow.py # Test: flujo completo end-to-end
    │
    ├── fixtures/                    # Datos de prueba reutilizables
    │   ├── __init__.py
    │   ├── extraction_fixtures.py   # Fixtures: extracciones de ejemplo
    │   └── template_fixtures.py     # Fixtures: templates de ejemplo
    │
    └── mocks/                       # Mocks reutilizables
        ├── __init__.py
        ├── mock_extraction_repository.py  # Mock: repositorio de extracciones
        ├── mock_ai_adapter.py             # Mock: servicio de IA
        └── mock_event_bus.py              # Mock: bus de eventos
```

## 🎯 Reglas de Dependencia (críticas para mantenibilidad)

```
┌─────────────────────────────────────────────────────────┐
│  API Layer (views, serializers)                         │
│  ↓ solo depende de ↓                                    │
├─────────────────────────────────────────────────────────┤
│  Application Layer (commands, queries, services)        │
│  ↓ solo depende de ↓                                    │
├─────────────────────────────────────────────────────────┤
│  Domain Layer (entities, value objects, services)       │
│  ↑ NO DEPENDE DE NADA ↑                                 │
├─────────────────────────────────────────────────────────┤
│  Infrastructure (repositories, adapters)                │
│  ↓ implementa interfaces de ↓                           │
└─────────────────────────────────────────────────────────┘
        ↑ inyectadas en ↑
   Application & API Layers
```

## 📋 Responsabilidades por Capa

### 1. **Domain Layer** 💎
- ✅ Lógica de negocio pura
- ✅ Validaciones de reglas de negocio
- ✅ Definición de interfaces (contratos)
- ❌ NO conoce Django, DB, HTTP, frameworks
- ❌ NO hace llamadas a servicios externos

### 2. **Application Layer** 🎯
- ✅ Coordina casos de uso
- ✅ Maneja transacciones
- ✅ Publica eventos
- ❌ NO contiene lógica de negocio
- ❌ NO accede directamente a DB (usa repositories)

### 3. **Infrastructure Layer** 🔧
- ✅ Implementa interfaces del dominio
- ✅ Acceso a base de datos (ORM)
- ✅ Integraciones con servicios externos
- ✅ Tareas asíncronas
- ❌ NO contiene lógica de negocio

### 4. **API Layer** 📡
- ✅ Maneja HTTP requests/responses
- ✅ Serialización/deserialización
- ✅ Validación de entrada (formato)
- ✅ Autenticación/autorización
- ❌ NO contiene lógica de negocio

### 5. **Interfaces Layer** 🌐
- ✅ Contratos públicos para otras apps
- ✅ DTOs para transferencia de datos
- ✅ Documentación de la API pública
- ❌ NO expone modelos internos
- ❌ NO expone entidades del dominio

## 🔄 Flujo de Comunicación entre Apps

```python
# ❌ NUNCA HACER ESTO (acoplamiento directo)
from apps.extraction.infrastructure.models import Extraction  # ¡MAL!

# ✅ SIEMPRE HACER ESTO (a través de interface)
from apps.extraction.interfaces.services.i_extraction_service import IExtractionService
from apps.extraction.interfaces.dtos.extraction_dto import ExtractionDTO

class MyService:
    def __init__(self, extraction_service: IExtractionService):
        self.extraction_service = extraction_service
    
    def do_something(self, extraction_id: UUID):
        # Solo usas DTOs, nunca modelos internos
        extraction = self.extraction_service.get_extraction_by_id(extraction_id)
```

## 📝 Checklist de Implementación

### Paso 1: Domain Layer
- [ ] Definir entidades principales
- [ ] Crear value objects
- [ ] Implementar servicios del dominio
- [ ] Definir excepciones del dominio
- [ ] Definir interfaces de repositorios
- [ ] **Tests unitarios del dominio**

### Paso 2: Infrastructure Layer
- [ ] Crear modelos Django (models.py)
- [ ] Implementar repositorios
- [ ] Crear adapters para servicios externos
- [ ] Configurar tareas Celery
- [ ] **Tests de integración con DB**

### Paso 3: Application Layer
- [ ] Implementar comandos (write operations)
- [ ] Implementar queries (read operations)
- [ ] Crear servicios de aplicación
- [ ] Configurar publicación de eventos
- [ ] **Tests de casos de uso**

### Paso 4: API Layer
- [ ] Crear serializers
- [ ] Implementar views/viewsets
- [ ] Configurar URLs
- [ ] Agregar filtros y paginación
- [ ] **Tests de API endpoints**

### Paso 5: Interfaces Layer
- [ ] Definir DTOs públicos
- [ ] Crear interface de servicio público
- [ ] Implementar servicio público
- [ ] Documentar interface pública
- [ ] **Tests de integración entre apps**

## 🎓 Ejemplo Rápido de Uso

```python
# En otra app (ej: interpretation)
from apps.extraction.interfaces.services.i_extraction_service import IExtractionService
from apps.extraction.interfaces.dtos.extraction_dto import ExtractionDTO

class InterpretationService:
    def __init__(self, extraction_service: IExtractionService):
        self.extraction_service = extraction_service
    
    def analyze_study(self, study_id: UUID):
        # Solo usas la interface pública
        extractions = self.extraction_service.get_extractions_by_study(study_id)
        
        # Trabajas con DTOs, no con modelos
        for extraction in extractions:
            print(f"Quality: {extraction.quality_score}")
```

Esta estructura garantiza:
- ✅ **Testeable**: Cada capa se testea independientemente
- ✅ **Mantenible**: Cambios internos no afectan otras apps
- ✅ **Escalable**: Fácil agregar funcionalidades
- ✅ **Type-safe**: Type hints en todos los contratos
- ✅ **Documentado**: Las interfaces son la documentación