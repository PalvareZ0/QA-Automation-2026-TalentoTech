"""
tests/test_carrito.py — Tests del carrito de compras (Clase 9).

Usa la fixture `usuario_logueado` (login automático) y prueba:
  - Agregar el primer producto actualiza el badge del carrito a 1.
  - El producto agregado aparece en la página del carrito.
  - El nombre del producto en el carrito coincide con el agregado.
"""
import pytest

from utils.logger import logger


@pytest.mark.smoke
@pytest.mark.carrito
def test_carrito_agregar_primer_producto(usuario_logueado, request):
    """Agregar el primer producto actualiza el badge del carrito a 1."""
    usuario_logueado.agregar_primer_producto()
    request.node.page_url = usuario_logueado.driver.current_url

    contador = usuario_logueado.obtener_contador_carrito()
    logger.info("Carrito: badge muestra %d tras agregar", contador)
    assert contador == 1, \
        f"El carrito debería mostrar 1, pero muestra: {contador}"


@pytest.mark.smoke
@pytest.mark.carrito
def test_carrito_verificar_producto_en_carrito(usuario_logueado, request):
    """El producto agregado debe aparecer en la página del carrito."""
    usuario_logueado.agregar_primer_producto()

    cart_page = usuario_logueado.ir_al_carrito()
    request.node.page_url = usuario_logueado.driver.current_url

    cantidad = cart_page.obtener_cantidad_productos()
    assert cantidad == 1, \
        f"Debería haber 1 producto en el carrito, pero hay: {cantidad}"


@pytest.mark.carrito
def test_carrito_nombre_producto_correcto(usuario_logueado, request):
    """El nombre del producto en el carrito coincide con el que se agregó."""
    info_producto = usuario_logueado.obtener_primer_producto_info()

    usuario_logueado.agregar_primer_producto()
    cart_page = usuario_logueado.ir_al_carrito()
    request.node.page_url = usuario_logueado.driver.current_url

    assert cart_page.contiene_producto(info_producto["nombre"]), \
        f"El producto '{info_producto['nombre']}' no se encontró en el carrito"
