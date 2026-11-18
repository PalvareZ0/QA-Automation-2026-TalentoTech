# tests/test_login.py

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
@pytest.mark.login
def test_login_exitoso_credenciales_validas(driver, credenciales_validas):
    """Login con credenciales validas redirige a la pagina de inventario."""
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        credenciales_validas["usuario"],
        credenciales_validas["password"]
    )

    inventory_page = InventoryPage(driver)
    assert inventory_page.esta_en_pagina_inventario(), "No se redirigio a inventory.html"


@pytest.mark.login
def test_login_verificar_titulo_post_login(driver, credenciales_validas):
    """Despues del login, el titulo de la pagina debe ser 'Swag Labs'."""
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        credenciales_validas["usuario"],
        credenciales_validas["password"]
    )

    assert "Swag Labs" in driver.title, f"Se esperaba 'Swag Labs' en el titulo, pero fue: {driver.title}"


@pytest.mark.login
def test_login_fallido_credenciales_invalidas(driver, credenciales_invalidas):
    """Login con credenciales invalidas muestra mensaje de error."""
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        credenciales_invalidas["usuario"],
        credenciales_invalidas["password"]
    )

    assert login_page.esta_error_visible(), "Deberia mostrarse un mensaje de error"


@pytest.mark.login
def test_login_usuario_bloqueado(driver, usuario_bloqueado):
    """Login con usuario bloqueado muestra mensaje de error."""
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        usuario_bloqueado["usuario"],
        usuario_bloqueado["password"]
    )

    assert login_page.esta_error_visible(), "Deberia mostrarse un mensaje de error para usuario bloqueado"
