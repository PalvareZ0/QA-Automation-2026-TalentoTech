"""
tests/test_login.py — Tests de login en SauceDemo (Clases 7-9).

Cubre:
  - Login exitoso con credenciales válidas (redirección a inventory.html).
  - Verificación del título 'Swag Labs' post-login.
  - Login fallido con credenciales inválidas (mensaje de error visible).
  - Login con usuario bloqueado (mensaje de error visible).
"""
import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import logger


@pytest.mark.smoke
@pytest.mark.login
def test_login_exitoso_credenciales_validas(driver, credenciales_validas, request):
    """Login con credenciales válidas redirige a la página de inventario."""
    logger.info("Login: probando credenciales válidas")
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        credenciales_validas["usuario"],
        credenciales_validas["password"],
    )
    request.node.page_url = driver.current_url

    inventory_page = InventoryPage(driver)
    assert inventory_page.esta_en_pagina_inventario(), \
        "No se redirigió a inventory.html"
    logger.info("Login exitoso verificado")


@pytest.mark.login
def test_login_verificar_titulo_post_login(driver, credenciales_validas, request):
    """Después del login, el título de la página debe ser 'Swag Labs'."""
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        credenciales_validas["usuario"],
        credenciales_validas["password"],
    )
    request.node.page_url = driver.current_url

    assert "Swag Labs" in driver.title, \
        f"Se esperaba 'Swag Labs' en el título, pero fue: {driver.title}"


@pytest.mark.login
def test_login_fallido_credenciales_invalidas(driver, credenciales_invalidas, request):
    """Login con credenciales inválidas muestra mensaje de error."""
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        credenciales_invalidas["usuario"],
        credenciales_invalidas["password"],
    )
    request.node.page_url = driver.current_url

    assert login_page.esta_error_visible(), \
        "Debería mostrarse un mensaje de error con credenciales inválidas"


@pytest.mark.login
def test_login_usuario_bloqueado(driver, usuario_bloqueado, request):
    """Login con usuario bloqueado muestra mensaje de error."""
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        usuario_bloqueado["usuario"],
        usuario_bloqueado["password"],
    )
    request.node.page_url = driver.current_url

    assert login_page.esta_error_visible(), \
        "Debería mostrarse un mensaje de error para usuario bloqueado"
