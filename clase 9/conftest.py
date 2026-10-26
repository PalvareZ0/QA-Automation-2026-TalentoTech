# conftest.py

import pytest
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="function")
def driver():
    """Fixture que proporciona un WebDriver configurado."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Descomentar para CI/CD
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)

    yield driver

    time.sleep(1)  # Pausa para ver el resultado final
    driver.quit()


@pytest.fixture
def credenciales_validas():
    """Credenciales validas para login."""
    return {
        "usuario": "standard_user",
        "password": "secret_sauce"
    }


@pytest.fixture
def credenciales_invalidas():
    """Credenciales invalidas para login."""
    return {
        "usuario": "usuario_invalido",
        "password": "clave_invalida"
    }


@pytest.fixture
def usuario_bloqueado():
    """Usuario bloqueado para login."""
    return {
        "usuario": "locked_out_user",
        "password": "secret_sauce"
    }


# ============================================================
# HOOK: Captura de pantalla al fallar un test
# ============================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            if not os.path.exists('reports/screenshots'):
                os.makedirs('reports/screenshots')

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name
            screenshot_path = f"reports/screenshots/{test_name}_{timestamp}.png"

            driver.save_screenshot(screenshot_path)
            print(f"\nCaptura de fallo guardada en: {screenshot_path}")
