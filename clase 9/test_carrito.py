# tests/test_carrito.py

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture
def inventory_page(driver, credenciales_validas):
    """Fixture: hace login y retorna InventoryPage listo para usar."""
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(
        credenciales_validas["usuario"],
        credenciales_validas["password"]
    )
    return InventoryPage(driver)


@pytest.mark.smoke
@pytest.mark.carrito
def test_carrito_agregar_primer_producto(inventory_page):
    """Agregar el primer producto actualiza el badge del carrito a 1."""
    inventory_page.agregar_primer_producto()
    contador = inventory_page.obtener_contador_carrito()
    assert contador == 1, f"El carrito deberia mostrar 1, pero muestra: {contador}"


@pytest.mark.smoke
@pytest.mark.carrito
def test_carrito_verificar_producto_en_carrito(inventory_page):
    """El producto agregado debe aparecer en la pagina del carrito."""
    inventory_page.agregar_primer_producto()

    # Navegar al carrito (InventoryPage.ir_al_carrito retorna CartPage)
    cart_page = inventory_page.ir_al_carrito()

    cantidad = cart_page.obtener_cantidad_productos()
    assert cantidad == 1, f"Deberia haber 1 producto en el carrito, pero hay: {cantidad}"


@pytest.mark.carrito
def test_carrito_nombre_producto_correcto(inventory_page):
    """El nombre del producto en el carrito coincide con el que se agrego."""
    # Obtener info del primer producto ANTES de agregarlo
    info_producto = inventory_page.obtener_primer_producto_info()

    # Agregar y navegar al carrito
    inventory_page.agregar_primer_producto()
    cart_page = inventory_page.ir_al_carrito()

    # Verificar que el nombre esta en el carrito
    assert cart_page.contiene_producto(info_producto["nombre"]), \
        f"El producto '{info_producto['nombre']}' no se encontro en el carrito"
