"""
features/steps/cart_steps.py — Conectores Python del carrito (QA-158, Tarea 3)
"""
from behave import then, when

from pages.inventory_page import InventoryPage
from utils.logger import logger


@when('agrego el producto "{producto}"')
def step_agregar_producto(context, producto):
    """Agrega un producto al carrito vía el Page Object."""
    InventoryPage(context.driver).agregar_producto(producto)
    logger.info("BDD: producto agregado '%s'", producto)


@then('el contador del carrito muestra "{cantidad}"')
def step_contador_carrito(context, cantidad):
    """Verifica el número que muestra el badge del carrito."""
    actual = InventoryPage(context.driver).contador_carrito()
    logger.info("BDD: contador del carrito = %s", actual)
    assert actual == cantidad, (
        f"Esperaba {cantidad} en el contador, muestra {actual}"
    )
