"""
conftest.py — Configuración global de Pytest (raíz del framework)

Vive en la RAÍZ del proyecto para que los hooks se apliquen a TODA la suite:
tests/ (UI), tests_api/ (API) y tests_behave/ (BDD wrapper).

Qué hay acá:
  1. Fixtures: driver (headless para CI/CD) + credenciales + datos CSV/JSON.
  2. Hook pytest_runtest_makereport: captura automática de screenshots en fallos UI.
  3. Columna "URL" en el reporte HTML (saber en qué página estaba cada test).
  4. Título y autor del reporte HTML.
"""
import base64
import os
import pathlib

import pytest

try:
    import pytest_html
except ImportError:  # si no está instalado, no rompemos la suite
    pytest_html = None

from utils.datos import leer_csv_login, leer_json_productos
from utils.logger import logger

AUTOR = "Pablo Alvarez — TalentoLab · QA Automation · Proyecto Final"

SCREENSHOTS_DIR = pathlib.Path("reports/screens")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1) FIXTURES — WebDriver y datos de prueba
# ============================================================

@pytest.fixture
def driver():
    """WebDriver de Chrome, headless por defecto (ideal para CI/CD).

    Para VER el navegador en local:
        HEADLESS=0 pytest ...
    """
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # evita crashes en CI

    _driver = webdriver.Chrome(options=options)
    _driver.implicitly_wait(5)
    _driver.maximize_window()

    yield _driver
    _driver.quit()  # teardown: SIEMPRE se cierra, sin procesos huérfanos


@pytest.fixture
def credenciales_validas():
    """Usuario válido de SauceDemo."""
    return {"usuario": "standard_user", "password": "secret_sauce"}


@pytest.fixture
def credenciales_invalidas():
    """Usuario inexistente (debe fallar)."""
    return {"usuario": "usuario_invalido", "password": "clave_invalida"}


@pytest.fixture
def usuario_bloqueado():
    """Usuario bloqueado por SauceDemo."""
    return {"usuario": "locked_out_user", "password": "secret_sauce"}


@pytest.fixture(scope="session")
def datos_login_csv():
    """Lee datos/login.csv una sola vez por sesión."""
    return leer_csv_login("datos/login.csv")


@pytest.fixture(scope="session")
def datos_productos_json():
    """Lee datos/productos.json una sola vez por sesión."""
    return leer_json_productos("datos/productos.json")


@pytest.fixture
def usuario_logueado(driver, credenciales_validas):
    """Hace login y retorna InventoryPage listo para tests de catálogo/carrito."""
    from pages.login_page import LoginPage
    from pages.inventory_page import InventoryPage

    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        credenciales_validas["usuario"],
        credenciales_validas["password"],
    )
    return InventoryPage(driver)


# ============================================================
# 2) HOOK DE CAPTURA INTELIGENTE
#    Se ejecuta después de cada fase (setup/call/teardown) de cada test.
#    - Copia la URL al reporte (columna URL).
#    - Captura screenshot SOLO cuando un test UI falla en la fase 'call'.
# ============================================================

@pytest.hookimpl(tryfirst=True, wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield

    if report.when == "call":
        # URL: la que guardó el test, o la actual del navegador (tests UI).
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

        # Captura solo si el test falló en la fase principal
        if report.failed:
            driver = item.funcargs.get("driver")
            if driver is not None and pytest_html is not None:
                file_name = SCREENSHOTS_DIR / f"{item.name}.png"
                try:
                    driver.save_screenshot(str(file_name))
                except Exception:
                    return report  # navegador caído: no romper el reporte

                with open(file_name, "rb") as f:
                    image_b64 = base64.b64encode(f.read()).decode("utf-8")
                screenshot = pytest_html.extras.image(image_b64, name="Screenshot")

                if hasattr(report, "extras"):  # pytest-html 4.x
                    report.extras.append(screenshot)
                else:                            # pytest-html 3.x (legacy)
                    report.extra = getattr(report, "extra", [])
                    report.extra.append(screenshot)

    return report


# ============================================================
# 3) COLUMNA "URL" EN EL REPORTE HTML
# ============================================================

def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>URL</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{getattr(report, 'page_url', '-')}</td>")


# ============================================================
# 4) TÍTULO Y AUTOR DEL REPORTE
# ============================================================

def pytest_html_report_title(report):
    report.title = "TalentoLab – Resumen de ejecución"


def pytest_html_results_summary(prefix, summary, postfix, session):
    prefix.append(
        f"<p><b>Autor:</b> {AUTOR}</p>"
        "<p><b>Suite:</b> UI (SauceDemo) + API (JSONPlaceholder) + BDD (Behave)</p>"
    )
