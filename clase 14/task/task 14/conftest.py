"""
conftest.py — Configuración global de Pytest
Clase 13: Reportes y Logging (pytest-html + capturas automáticas)

Qué vive acá:
  1. Fixture `driver`  → navegador compartido para los tests UI
  2. Hook de captura   → screenshot automático solo cuando falla un test UI
  3. Columna "URL"     → muestra en qué página estaba cada test
  4. Título y autor    → personalización del reporte HTML
"""
import base64
import os
import pathlib

import pytest

try:
    import pytest_html
except ImportError:  # pragma: no cover
    pytest_html = None

# ✏️ EDITÁ ESTA LÍNEA con tu nombre (aparece en el reporte HTML)
AUTOR = "Tu Nombre — TalentoLab · QA Automation · Clase 13"

# 📁 Carpeta donde se guardan las capturas (se crea sola)
SCREENSHOTS_DIR = pathlib.Path("reports/screens")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------
# 1) FIXTURE DRIVER — navegador para los tests UI
#    Selenium Manager (Selenium 4.6+) descarga el driver solo.
# ------------------------------------------------------------------
@pytest.fixture
def driver():
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    # Headless por defecto (ideal para CI/CD). Para VER el navegador:
    #   HEADLESS=0 pytest ...
    if os.getenv("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    _driver = webdriver.Chrome(options=options)
    _driver.implicitly_wait(5)      # espera implícita global (red de seguridad)
    _driver.maximize_window()

    yield _driver                   # el test usa el navegador

    _driver.quit()                  # teardown: SIEMPRE se cierra


# ------------------------------------------------------------------
# 2) HOOK DE CAPTURA INTELIGENTE
#    Se ejecuta después de cada fase (setup/call/teardown) de cada test.
#    - Copia la URL de la página a la columna "URL" del reporte.
#    - Captura screenshot SOLO cuando un test UI falla en la fase 'call'.
# ------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield  # dejamos que Pytest genere el reporte de la fase

    if report.when == "call":
        # URL del test: la que el test guardó en request.node.page_url,
        # o (en tests UI) la URL actual del navegador, automáticamente.
        page_url = getattr(item, "page_url", None)
        if page_url is None:
            driver = item.funcargs.get("driver")
            if driver is not None:
                try:
                    page_url = driver.current_url
                except Exception:
                    page_url = None
        if page_url:
            report.page_url = page_url

        # 🎯 Solo capturamos cuando el test FALLÓ en la fase principal
        if report.failed:
            driver = item.funcargs.get("driver")
            if driver is not None and pytest_html is not None:
                file_name = SCREENSHOTS_DIR / f"{item.name}.png"
                try:
                    driver.save_screenshot(str(file_name))
                except Exception:
                    return report  # navegador caído: no rompemos el reporte

                # 📋 Adjuntamos la captura DENTRO del reporte (base64)
                with open(file_name, "rb") as f:
                    image_b64 = base64.b64encode(f.read()).decode("utf-8")
                screenshot = pytest_html.extras.image(image_b64, name="Screenshot")

                if hasattr(report, "extras"):       # pytest-html 4.x
                    report.extras.append(screenshot)
                else:                               # pytest-html 3.x (legacy)
                    report.extra = getattr(report, "extra", [])
                    report.extra.append(screenshot)

    return report  # SIEMPRE devolver el reporte (obligatorio con wrapper=True)


# ------------------------------------------------------------------
# 3) COLUMNA "URL" EN LA TABLA DE RESULTADOS
# ------------------------------------------------------------------
def pytest_html_results_table_header(cells):
    """Añade una columna 'URL' justo después de la columna 'Test'."""
    cells.insert(2, "<th>URL</th>")


def pytest_html_results_table_row(report, cells):
    """Rellena la columna con la URL guardada en report.page_url."""
    cells.insert(2, f"<td>{getattr(report, 'page_url', '-')}</td>")


# ------------------------------------------------------------------
# 4) TÍTULO Y AUTOR DEL REPORTE
# ------------------------------------------------------------------
def pytest_html_report_title(report):
    report.title = "TalentoLab – Resumen de ejecución"


def pytest_html_results_summary(prefix, summary, postfix, session):
    """Agrega el autor y la descripción en el encabezado del reporte."""
    prefix.append(
        f"<p><b>Autor:</b> {AUTOR}</p>"
        "<p><b>Suite:</b> UI (SauceDemo) + API (JSONPlaceholder)</p>"
    )
