"""
tests/test_catalogo.py — Tests del catálogo de inventario (Clase 9-10).

Usa la fixture `usuario_logueado` (definida en conftest.py raíz) que hace
login y devuelve un InventoryPage listo para usar.
"""
import pytest

from utils.logger import logger


@pytest.mark.smoke
@pytest.mark.catalogo
def test_catalogo_titulo_correcto(usuario_logueado, request):
    """El título del catálogo debe ser 'Products'."""
    titulo = usuario_logueado.obtener_titulo()
    request.node.page_url = driver_url(usuario_logueado)
    logger.info("Catálogo: título visible '%s'", titulo)

    assert titulo == "Products", \
        f"Se esperaba 'Products', pero se obtuvo: {titulo}"


@pytest.mark.smoke
@pytest.mark.catalogo
def test_catalogo_hay_productos_visibles(usuario_logueado, request):
    """El catálogo debe tener productos visibles."""
    cantidad = usuario_logueado.obtener_cantidad_productos()
    request.node.page_url = driver_url(usuario_logueado)
    logger.info("Catálogo: %d productos visibles", cantidad)

    assert cantidad > 0, "No hay productos visibles en el inventario"


@pytest.mark.catalogo
def test_catalogo_primer_producto_tiene_info(usuario_logueado, request):
    """El primer producto debe tener nombre y precio."""
    info = usuario_logueado.obtener_primer_producto_info()
    request.node.page_url = driver_url(usuario_logueado)

    assert "nombre" in info and info["nombre"], \
        "El primer producto no tiene nombre"
    assert "precio" in info and info["precio"], \
        "El primer producto no tiene precio"


def driver_url(inventory_page):
    """Helper pequeño para leer la URL actual del driver del page object."""
    try:
        return inventory_page.driver.current_url
    except Exception:
        return None
