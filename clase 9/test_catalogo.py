# tests/test_catalogo.py

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
@pytest.mark.catalogo
def test_catalogo_titulo_correcto(inventory_page):
    """El titulo del catalogo debe ser 'Products'."""
    titulo = inventory_page.obtener_titulo()
    assert titulo == "Products", f"Se esperaba 'Products', pero se obtuvo: {titulo}"


@pytest.mark.smoke
@pytest.mark.catalogo
def test_catalogo_hay_productos_visibles(inventory_page):
    """El catalogo debe tener productos visibles."""
    cantidad = inventory_page.obtener_cantidad_productos()
    assert cantidad > 0, "No hay productos visibles en el inventario"


@pytest.mark.catalogo
def test_catalogo_primer_producto_tiene_info(inventory_page):
    """El primer producto debe tener nombre y precio."""
    info = inventory_page.obtener_primer_producto_info()
    assert "nombre" in info and info["nombre"], "El primer producto no tiene nombre"
    assert "precio" in info and info["precio"], "El primer producto no tiene precio"
