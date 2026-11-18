"""
tests/test_carrito_json.py — Tests de carrito con datos externos (Clase 10).

Lee la lista de productos desde datos/productos.json y, mediante
parametrización de Pytest, ejecuta un test por cada producto.

Flujo:
  1. Ya estamos logueados (fixture usuario_logueado).
  2. Agregar el producto específico por nombre (desde el JSON).
  3. Verificar que el badge del carrito se actualizó.
  4. Navegar al carrito y verificar que el producto está.
"""
import pytest

from utils.datos import leer_json_productos
from utils.logger import logger

# Cargar datos del JSON al nivel del módulo (una sola vez)
PRODUCTOS = leer_json_productos("datos/productos.json")
NOMBRES_PRODUCTOS = [prod["nombre"] for prod in PRODUCTOS]


@pytest.mark.carrito
@pytest.mark.parametrize("producto", PRODUCTOS, ids=NOMBRES_PRODUCTOS)
def test_agregar_producto_desde_json(usuario_logueado, producto, request):
    """Agrega cada producto del JSON al carrito y verifica que aparece."""
    inventory_page = usuario_logueado
    nombre = producto["nombre"]
    logger.info("Carrito JSON: agregando '%s'", nombre)

    inventory_page.agregar_producto_por_nombre(nombre)
    request.node.page_url = inventory_page.driver.current_url

    contador = inventory_page.obtener_contador_carrito()
    assert contador >= 1, \
        f"El carrito debería tener al menos 1 producto tras agregar '{nombre}'"

    cart_page = inventory_page.ir_al_carrito()
    assert cart_page.contiene_producto(nombre), \
        f"El producto '{nombre}' no se encontró en el carrito"


@pytest.mark.smoke
@pytest.mark.carrito
def test_carrito_smoke(usuario_logueado, request):
    """Smoke test: funcionalidad básica del carrito."""
    inventory_page = usuario_logueado

    inventory_page.agregar_primer_producto()
    request.node.page_url = inventory_page.driver.current_url

    contador = inventory_page.obtener_contador_carrito()
    assert contador == 1, \
        f"Smoke test: carrito debería mostrar 1, muestra {contador}"

    cart_page = inventory_page.ir_al_carrito()
    cantidad = cart_page.obtener_cantidad_productos()
    assert cantidad == 1, \
        f"Smoke test: debería haber 1 producto en carrito, hay {cantidad}"
