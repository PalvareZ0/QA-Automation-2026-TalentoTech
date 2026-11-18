# tests/test_carrito_json.py

import pytest
from pages.inventory_page import InventoryPage
from utils.datos import leer_json_productos


# Cargar datos del JSON al nivel del modulo
PRODUCTOS = leer_json_productos("datos/productos.json")
NOMBRES_PRODUCTOS = [prod["nombre"] for prod in PRODUCTOS]


@pytest.mark.carrito
@pytest.mark.parametrize("producto", PRODUCTOS,
                         ids=NOMBRES_PRODUCTOS)
def test_agregar_producto_desde_json(usuario_logueado, producto):
    """
    Test parametrizado que agrega cada producto del JSON al carrito
    y verifica que aparece en la pagina del carrito.

    Flujo:
    1. Ya estamos logueados (fixture usuario_logueado)
    2. Agregar el producto especifico por nombre
    3. Navegar al carrito
    4. Verificar que el producto esta en el carrito
    """
    inventory_page = usuario_logueado

    # Agregar el producto por nombre
    inventory_page.agregar_producto_por_nombre(producto["nombre"])

    # Verificar que el badge se actualizo
    contador = inventory_page.obtener_contador_carrito()
    assert contador >= 1, \
        f"El carrito deberia tener al menos 1 producto tras agregar '{producto['nombre']}'"

    # Navegar al carrito y verificar
    cart_page = inventory_page.ir_al_carrito()
    assert cart_page.contiene_producto(producto["nombre"]), \
        f"El producto '{producto['nombre']}' no se encontro en el carrito"


@pytest.mark.smoke
@pytest.mark.carrito
def test_carrito_smoke(usuario_logueado):
    """Test de smoke: verifica funcionalidad basica del carrito."""
    inventory_page = usuario_logueado

    # Agregar el primer producto
    inventory_page.agregar_primer_producto()

    # Verificar badge
    contador = inventory_page.obtener_contador_carrito()
    assert contador == 1, f"Smoke test: carrito deberia mostrar 1, muestra {contador}"

    # Navegar al carrito y verificar que hay items
    cart_page = inventory_page.ir_al_carrito()
    cantidad = cart_page.obtener_cantidad_productos()
    assert cantidad == 1, f"Smoke test: deberia haber 1 producto en carrito, hay {cantidad}"
