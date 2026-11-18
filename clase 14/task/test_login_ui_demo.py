"""
Tests UI de demostración sobre SauceDemo (https://www.saucedemo.com)
Clase 13 — verifican que el reporte HTML, la columna URL, las capturas
automáticas y el logging funcionen de punta a punta.

👉 Cuando pases estos tests a tu framework con Page Objects, mantené la
   línea  request.node.page_url = driver.current_url  para que la columna
   URL del reporte siga llenándose.
"""
import pytest
from selenium.webdriver.common.by import By

from utils.logger import logger

BASE_URL = "https://www.saucedemo.com"


@pytest.mark.ui
def test_login_usuario_valido(driver, request):
    """Login con standard_user → redirige a inventory.html."""
    logger.info("Iniciando login con usuario: %s", "standard_user")

    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # ✅ Guarda la URL actual para la columna 'URL' del reporte
    request.node.page_url = driver.current_url

    logger.info("Verificando redirección a inventory.html")
    assert "inventory.html" in driver.current_url
    logger.info("Login exitoso, test terminado")


@pytest.mark.ui
def test_login_invalido_muestra_error(driver, request):
    """Login con credenciales inválidas → mensaje de error visible."""
    logger.info("Iniciando login con credenciales inválidas")

    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("usuario_malo")
    driver.find_element(By.ID, "password").send_keys("password_malo")
    driver.find_element(By.ID, "login-button").click()

    request.node.page_url = driver.current_url

    error = driver.find_element(By.CSS_SELECTOR, 'h3[data-test="error"]')
    assert "Username and password do not match" in error.text
    logger.info("Mensaje de error mostrado correctamente")


@pytest.mark.ui
def test_demo_fallo_con_captura(driver, request):
    """
    ⚠️ ESTE TEST FALLA A PROPÓSITO.
    Sirve para que veas en el reporte HTML:
      - la fila roja del test fallido
      - la captura de pantalla automática adjunta
      - la URL donde estaba el navegador
    Bórralo cuando agregues tus tests reales.
    """
    logger.info("Ejecutando test de demostración (falla a propósito)")

    driver.get(BASE_URL)
    request.node.page_url = driver.current_url

    assert "inventory.html" in driver.current_url, (
        "Fallo a propósito: estamos en el login, no en el inventario. "
        "Mirá la captura automática en el reporte."
    )
