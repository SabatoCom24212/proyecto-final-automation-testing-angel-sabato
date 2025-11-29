# Entrega Trabajo Final Integrador | Automatización QA | C25247

## Framework de Automatización de Pruebas

Framework completo de automatización que combina pruebas de UI (Selenium) y API (Requests) con arquitectura escalable y CI/CD integrado.

## Características Principales

### Tests de UI (6 métodos parametrizados)

- **Patrón Page Object Model (POM)** con separación clara de responsabilidades
- **Aislamiento total** mediante fixtures de scope `function` (cada test obtiene un navegador limpio)
- **Estrategias de espera robustas** con `WebDriverWait` y condiciones explícitas
- **Screenshots automáticos** en fallos, embebidos en reportes HTML
- **Gestión inteligente del estado** con método `reset_app_state()` que implementa múltiples estrategias de limpieza
- **Helpers reutilizables** para evitar duplicación (ej: `wait_for_cart_count()`, `_configurar_chrome_options()`)
- Limpieza automática de cookies, localStorage y sessionStorage entre tests

### Tests de API (+20 métodos en 8 clases)

- **Cobertura exhaustiva**: CRUD completo (POST, GET, PUT, PATCH, DELETE)
- **Flujos complejos**: Ciclos de vida completos de recursos, relaciones entre entidades
- **Escenarios negativos**: Validación de datos inválidos, edge cases, recursos inexistentes
- **Validaciones avanzadas**: Integridad de datos, tipos, paginación, filtros, relaciones
- **Tests de rendimiento**: Medición de tiempos de respuesta, requests concurrentes
- **Cliente HTTP reutilizable** con métodos helpers (`get_all_todos()`, `get_user_posts()`, etc.)
- **Data-driven testing** con datos parametrizados desde JSON

### CI/CD y Reportes

- **GitHub Actions** configurado con ejecución automática en push/PR
- **Cancelación de workflows duplicados** para optimizar recursos
- **Ejecución secuencial** de tests para máxima estabilidad
- **Retry automático** con `pytest-rerunfailures` (2 reintentos con 1s de delay)
- **Reportes HTML interactivos** con `pytest-html` (duración, logs, screenshots, metadata)
- **Logging unificado** en archivo único con modo append para toda la sesión
- **Artefactos** con retención de 30 días (reportes, logs, screenshots)
- Instalación automática de Chrome y ChromeDriver en CI

### Arquitectura y Diseño

- **Código DRY** (Don't Repeat Yourself): Helpers y utilidades centralizadas
- **Parametrización extensiva** con `@pytest.mark.parametrize` para cobertura de múltiples escenarios
- **Utilidades centralizadas**:
  - `TestLogger`: Sistema de logging estructurado con handlers únicos
  - `Config`: Gestión centralizada de configuración y variables de entorno
  - `DataLoader`: Carga de datos desde JSON con métodos específicos
- **Separación de responsabilidades**:
  - `pages.py`: Page Objects con BasePage reutilizable
  - `tests/`: Suites organizadas por tipo (UI/API)
  - `data/`: Datos externos en JSON
  - `utils.py`: Funciones helper (captura de pantalla, limpieza, logging)
- **Fixtures avanzadas**: `logged_in_driver` que garantiza estado limpio pre-test

## Estructura del Proyecto

```plaintext
automation-framework/
├── .github/
│   └── workflows/ 
│       └── tests.yml               # CI/CD con GitHub Actions
├── data/
│   ├── test_data.json              # Datos para tests UI (usuarios, productos, checkout)
│   └── test_data_api.json          # Datos para tests API (CRUD, edge cases, flujos)
├── logs/
│   └── pytest_execution.log        # Log único consolidado de toda la sesión
├── reports/
│   └── report.html                 # Reporte HTML interactivo con pytest-html
├── screenshots/                    # Screenshots de tests fallidos (timestamped)
├── tests/
│   ├── ui/
│   │   ├── conftest.py             # Fixtures: driver, logged_in_driver, hooks
│   │   └── test_ui.py              # 6 tests de UI parametrizados
│   └── api/
│       ├── conftest.py             # Fixtures: api_client con métodos HTTP
│       └── test_api.py             # +20 tests API en 8 clases
├── conftest.py                     # Para que pytest detecte fixtures globales
├── pages.py                        # Page Objects: BasePage, LoginPage, InventoryPage, CartPage, CheckoutPage
├── utils.py                        # TestLogger, Config, DataLoader, helpers (screenshot, limpieza)
├── requirements.txt                # Dependencias del proyecto
├── pytest.ini                      # Configuración pytest (markers, paths, reportes)
└── README.md
```

## Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/SabatoCom24212/proyecto-final-automation-testing-angel-sabato.git
cd proyecto-final-automation-testing-angel-sabato
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución de Tests

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar solo tests de UI

```bash
pytest tests/ui/
```

### Ejecutar solo tests de API

```bash
pytest tests/api/
```

### Ejecutar tests con marcadores específicos

```bash
# Solo tests marcados como 'smoke'
pytest -m smoke

# Solo tests de UI
pytest -m ui

# Solo tests de API
pytest -m api
```

### Ejecutar en modo headless

```bash
# Windows (PowerShell)
$env:HEADLESS="true"; pytest tests/ui/

# Linux/Mac
HEADLESS=true pytest tests/ui/
```

## CI/CD con GitHub Actions

### Triggers

El workflow `.github/workflows/tests.yml` se ejecuta automáticamente en:

- Push a ramas: `main`, `master`, `develop`
- Pull Requests hacia estas ramas
- Ejecución manual desde GitHub Actions UI

### Características del workflow

- **Concurrencia**: Cancela ejecuciones previas del mismo workflow para la misma rama
- **Timeout**: 30 minutos máximo por job
- **Ambiente**: Ubuntu latest con Python 3.13.7
- **Cache**: Cache de dependencias pip para acelerar builds
- **Navegador**: Chrome stable con ChromeDriver gestionado automáticamente
- **Ejecución**: Tests secuenciales con retry (2 reintentos, 1s de delay)
- **Reportes**: JUnit XML para integración con GitHub

### Artefactos generados

Después de cada ejecución, se pueden descargar los siguientes artefactos (retención: 30 días):

1. **test-artifacts**: Contiene
   - `reports/`: Reportes HTML con resultados detallados
   - `logs/`: Log único consolidado de toda la ejecución
   - `screenshots/`: Screenshots de tests fallidos (solo UI)

### Ver resultados

1. Ir a la pestaña **Actions** en GitHub
2. Seleccionar la ejecución deseada
3. Ver resumen de tests en la página del workflow
4. Descargar artefactos en la sección **Artifacts** (parte inferior)

## Reportes

### Reporte HTML (`reports/report.html`)

Generado automáticamente por `pytest-html`, incluye:

- **Resumen ejecutivo**: Tests passed/failed/skipped, duración total
- **Tabla de resultados**: Cada test con status, duración, error (si aplica)
- **Logs detallados**: Por test, expandibles en la UI
- **Screenshots**: Embebidos inline para tests fallidos (UI)
- **Metadata**: Sistema operativo, Python version, navegador

**Características**:

- Modo `--self-contained-html`: Todo en un solo archivo HTML (portable)
- Ordenado por duración para identificar tests lentos
- Filtros interactivos por status

### Log unificado (`logs/pytest_execution.log`)

Archivo único que consolida TODOS los logs de la sesión:

- **Modo append**: Acumula logs de múltiples ejecuciones
- **Formato estructurado**: `[timestamp] - [logger_name] - [level] - [file:line] - [message]`
- **Niveles**:
  - `INFO`: Pasos principales de tests, aserciones
  - `DEBUG`: Acciones detalladas, búsqueda de elementos
  - `WARNING`: Screenshots, problemas no críticos
  - `ERROR`: Fallos de tests

**Métodos del logger**:

- `test_start(name)` / `test_end(name, status)`
- `step(description)`: Para pasos del test
- `action(description)`: Para acciones específicas
- `assertion(description, result)`: Para registrar aserciones
- `api_request(method, url, status_code)`: Para requests API

## Configuración

### Variables de entorno

```bash
# Ejecutar en modo headless (sin interfaz gráfica)
export HEADLESS=true

# Modo CI (fuerza headless + optimizaciones)
export CI=true

# En Windows PowerShell
$env:HEADLESS="true"
$env:CI="true"
```

### Marcadores personalizados

Ejecutar subconjuntos de tests:

```bash
pytest -m ui          # Solo tests de UI
pytest -m api         # Solo tests de API
pytest -m smoke       # Solo smoke tests
pytest -m "not slow"  # Excluir tests lentos
```

## Mejores Prácticas Implementadas

### Aislamiento de Tests

- **Function-scoped fixtures**: Cada test UI obtiene un navegador completamente nuevo
- **Limpieza pre-test**: `logged_in_driver` garantiza carrito vacío antes de cada test
- **Limpieza post-test**: Cookies, localStorage y sessionStorage eliminados

### Manejo de Esperas

- **Esperas explícitas**: `WebDriverWait` con condiciones específicas
- **No esperas implícitas mezcladas**: Solo timeouts configurados en fixtures
- **Helper `wait_for_cart_count()`**: Evita código duplicado para esperar actualizaciones del carrito

### Gestión de Errores

- **Try-catch en fixtures**: Captura de screenshots garantizada incluso si el test explota
- **Logging estructurado**: Trazabilidad completa de fallos
- **Múltiples estrategias de limpieza**: `reset_app_state()` tiene fallback si el menú falla

### Código Limpio

- **Helpers reutilizables**: `capturar_pantalla()`, `limpiar_navegador()`, `_configurar_chrome_options()`
- **Page Objects con BasePage**: Métodos comunes heredados (find_element, click_element, etc.)
- **Cliente API con helpers**: Métodos específicos (`get_all_todos()`) evitan URLs mágicas

### Data-Driven Testing

- **JSON externos**: Separación de datos y lógica
- **Parametrización**: Un método de test cubre múltiples escenarios
- **DataLoader centralizado**: Métodos específicos (`get_usuarios_validos()`) en lugar de acceso directo al JSON
