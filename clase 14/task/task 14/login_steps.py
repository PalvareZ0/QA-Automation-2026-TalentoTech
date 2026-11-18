"""
features/steps/login_steps.py — Conectores Python del login (QA-158, Tarea 3)
Cada step reutiliza los Page Objects (LoginPage / InventoryPage) y registra
logs informativos con utils.logger.
"""
from behave import given, then, when

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.logger import logger


@given('que estoy en la página de login')
def step_pagina_login(context):
    """Abre la página de login usando el Page Object."""
    context.login_page = LoginPage(context.driver)
    context.login_page.abrir()
    logger.info("BDD: página de login abierta")


@given('que inicié sesión como "{usuario}"')
def step_login_automatico(context, usuario):
    """Login completo (lo usa el Background del carrito)."""
    context.login_page = LoginPage(context.driver)
    context.login_page.login_completo(usuario, "secret_sauce")
    logger.info("BDD: login automático como %s", usuario)


@given('estoy en la página de inventario')
def step_pagina_inventario(context):
    """Verifica que el login redirigió al inventario."""
    url = context.driver.current_url
    assert "inventory.html" in url, f"URL actual: {url}"
    logger.info("BDD: en la página de inventario")


@when('ingreso usuario "{usuario}" y clave "{clave}"')
def step_ingreso_credenciales(context, usuario, clave):
    """Completa el formulario y envía las credenciales.
    La palabra 'vacío' en la tabla significa: dejar el campo sin completar."""
    usuario = None if usuario.lower() == "vacío" else usuario
    clave = None if clave.lower() == "vacío" else clave
    context.login_page.ingresar_credenciales(usuario, clave)
    context.login_page.hacer_click_login()
    logger.info("BDD: credenciales enviadas (usuario='%s')", usuario or "(vacío)")


@then('la URL contiene "{texto}"')
def step_url_contiene(context, texto):
    """Verifica que la URL actual contiene el texto esperado."""
    url = context.driver.current_url
    logger.info("BDD: verificando URL %s", url)
    assert texto in url, f"Esperaba '{texto}' dentro de la URL {url}"


@then('veo el título "{titulo}"')
def step_veo_titulo(context, titulo):
    """Verifica el título visible del inventario."""
    visible = InventoryPage(context.driver).titulo()
    logger.info("BDD: título visible '%s'", visible)
    assert visible == titulo, f"Esperaba '{titulo}', visible '{visible}'"


@then('veo el mensaje de error "{mensaje}"')
def step_mensaje_error(context, mensaje):
    """Verifica que aparece el mensaje de error esperado."""
    texto = context.login_page.texto_error()
    logger.info("BDD: mensaje de error visible '%s'", texto)
    assert mensaje in texto, f"Esperaba '{mensaje}' dentro de '{texto}'"
