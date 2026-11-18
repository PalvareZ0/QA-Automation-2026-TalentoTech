# 🚀 Framework de Automatización de Pruebas — TalentoLab

Framework profesional de automatización de pruebas QA que cubre **UI**, **API** y
**BDD**, con reportes HTML, logging, capturas automáticas y pipeline de CI/CD.

> Proyecto Final — Curso QA Automation Testing (TalentoTech 2026)

---

## 📌 Propósito del proyecto

Demostrar un framework de testing completo en Python que combine:

- **Pruebas de UI** con Selenium WebDriver sobre [SauceDemo](https://www.saucedemo.com/).
- **Pruebas de API** con la librería Requests sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com/) y [ReqRes](https://reqres.in/).
- **Pruebas BDD** con Behave + Gherkin (especificaciones ejecutables legibles por todo el equipo).
- **Reportes HTML** y **logging centralizado** con capturas automáticas en fallos.
- **CI/CD** con GitHub Actions (cada `push` ejecuta toda la suite automáticamente).

---

## 🛠️ Tecnologías utilizadas

| Herramienta          | Para qué se usa                                  |
| -------------------- | ------------------------------------------------ |
| Python 3.12          | Lenguaje principal                               |
| Pytest               | Framework de testing y generación de reportes    |
| Selenium WebDriver   | Automatización del navegador (Chrome)            |
| Requests             | Pruebas de API REST                              |
| Behave + Gherkin     | BDD: especificaciones ejecutables                |
| Faker                | Generación de datos aleatorios                   |
| pytest-html          | Reportes HTML autocontenidos                     |
| pytest-check         | Soft-asserts (no cortan en el primer fallo)      |
| pytest-rerunfailures | Reintentos automáticos para tests flaky          |
| GitHub Actions       | CI/CD: ejecución automática en cada push         |

---

## 📁 Estructura del proyecto

```
proyecto-final-automation-testing-[nombre-apellido]/
├── pages/                     # Page Object Model (Clase 9)
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── tests/                     # Tests UI (Clases 7-10)
│   ├── test_login.py
│   ├── test_login_faker.py
│   ├── test_login_csv.py
│   ├── test_catalogo.py
│   ├── test_carrito.py
│   └── test_carrito_json.py
├── tests_api/                 # Tests API (Clases 11-12)
│   ├── test_login_api.py
│   ├── test_users_api.py
│   ├── test_create_user_api.py
│   ├── test_post_lifecycle.py
│   └── test_api_demo.py
├── features/                  # BDD con Behave (Clase 14)
│   ├── login.feature
│   ├── cart.feature
│   ├── operaciones.feature
│   ├── environment.py         # Hooks globales
│   └── steps/                  # Step definitions
├── tests_behave/              # Wrapper: Behave desde Pytest
│   └── test_behave_suite.py
├── datos/                     # Datos externos (Clase 10)
│   ├── login.csv
│   └── productos.json
├── utils/                     # Helpers
│   ├── datos.py               # Lectores de CSV y JSON
│   ├── logger.py              # Logger centralizado con rotación
│   └── operaciones.py         # Lógica de ejemplo (BDD sin navegador)
├── reports/                   # Reportes HTML + capturas (gitignored)
├── logs/                      # Logs de la suite (gitignored)
├── .github/workflows/ci.yml   # Pipeline de CI/CD (Clase 15)
├── conftest.py                # Hooks + fixtures globales
├── pytest.ini                 # Configuración de Pytest
├── behave.ini                 # Configuración de Behave
├── requirements.txt           # Dependencias
├── .gitignore
└── README.md                  # Este archivo
```

---

## ⚙️ Instalación

### 1) Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/proyecto-final-automation-testing-nombre-apellido.git
cd proyecto-final-automation-testing-nombre-apellido
```

### 2) Crear y activar un entorno virtual (recomendado)

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3) Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4) Tener Google Chrome instalado

Selenium Manager (incluido en Selenium 4.6+) descarga ChromeDriver
automáticamente; solo necesitás el navegador Chrome.

---

## 💻 Cómo ejecutar las pruebas

Todos los comandos se ejecutan desde la raíz del proyecto.

### Ejecutar TODA la suite (UI + API + BDD)

```bash
pytest
```

Esto genera `reports/pytest_report.html` automáticamente (configurado en `pytest.ini`).

### Ejecutar solo tests UI

```bash
pytest tests/ -v
```

### Ejecutar solo tests de API

```bash
pytest tests_api/ -v
```

### Ejecutar por marcadores (markers)

```bash
pytest -m smoke          # solo tests críticos
pytest -m api            # solo tests de API
pytest -m "ui and smoke" # tests UI críticos
pytest -m bdd            # wrapper de Behave desde Pytest
```

### Ejecutar Behave directamente (BDD puro)

```bash
behave -t @smoke         # solo escenarios @smoke
behave -t @regression    # solo @regression
behave                    # toda la suite BDD
```

### Ver el navegador (modo no headless)

Por defecto los tests UI corren en modo **headless** (sin ventana visible,
ideal para CI/CD). Para ver el navegador en local:

```bash
HEADLESS=0 pytest tests/
```

---

## 📊 Cómo interpretar los reportes

Después de cada ejecución, abrí `reports/pytest_report.html` en tu navegador.
El reporte muestra:

- **Tabla de resultados**: cada test con su estado (✅/❌) y duración.
- **Columna URL**: en qué página estaba el navegador cuando corrió el test.
- **Capturas automáticas**: si un test UI falla, su screenshot queda incrustado
  en el reporte (gracias al hook `pytest_runtest_makereport`).
- **Traceback completo**: del error, para depurar.

Para Behave, los reportes quedan en `reports/behave.html` (HTML autocontenido)
y `reports/behave.json` (para pipelines).

Los logs detallados (paso a paso con timestamps) están en `logs/suite.log`.

---

## 🔧 Configuración de CI/CD

El pipeline vive en `.github/workflows/ci.yml` y se dispara en cada `push` o
`pull_request` a `main`/`develop`. Hace lo siguiente:

1. Instala Python 3.12 y Google Chrome.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Ejecuta toda la suite (Pytest + Behave).
4. Sube `reports/` y `logs/` como artefactos descargables (90 días de retención).

### Estado del pipeline (badge)

Agregá esta línea al inicio de tu README (reemplazando usuario y repo):

```markdown
![CI Status](https://github.com/TU_USUARIO/TU_REPOSITORIO/actions/workflows/ci.yml/badge.svg)
```

---

## ✅ Cobertura de pruebas

### UI (SauceDemo) — `tests/`

- Login exitoso con credenciales válidas.
- Login fallido con credenciales inválidas.
- Login con usuario bloqueado.
- Login con datos aleatorios de Faker (incluye casos de inyección).
- Login parametrizado desde CSV (5 casos).
- Catálogo: título 'Products', productos visibles, info del primer producto.
- Carrito: agregar primer producto, verificar producto en carrito, nombre correcto.
- Carrito parametrizado con JSON (un test por cada producto).

### API (JSONPlaceholder + ReqRes) — `tests_api/`

- Login ReqRes (válido → 200+token, sin password → 400).
- GET de usuarios con validación de estructura y contenido.
- POST crear usuario parametrizado (4 casos).
- Ciclo de vida completo: POST → PATCH → DELETE (encadenado).
- Soft-asserts y retry de tests flaky (demo de observabilidad).

### BDD (Behave) — `features/`

- `login.feature`: login exitoso + esquema de errores (4 casos).
- `cart.feature`: agregar 1 producto, agregar 2 productos.
- `operaciones.feature`: multiplicación parametrizada (4 casos).
- `demo_fallo.feature`: escenario que falla a propósito (verifica el hook de captura).

---

## 📝 Convenciones del proyecto

- **POM**: cada página es una clase con locators privados (`_LOCATOR`), métodos
  de acción y helpers de consulta (sin asserts dentro de las páginas).
- **Method chaining**: los métodos de página retornan `self` para sintaxis fluida.
- **Esperas explícitas** para pasos críticos, implícita global de 5s como red de seguridad.
- **Headless por defecto** en CI/CD (variable de entorno `HEADLESS`).
- **Datos externos**: CSV y JSON en `datos/`, nunca hardcodeados en los tests.
- **Markers**: `@smoke`, `@regression`, `@ui`, `@api`, `@e2e`, `@bdd`, `@flaky`.

---

## 👤 Autor

**Pablo Alvarez** — TalentoLab · QA Automation · 2026
