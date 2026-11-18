"""
tests/test_login_csv.py — Login parametrizado con datos de CSV (Clase 10).

Lee los casos de login desde datos/login.csv y ejecuta un test por cada
fila. Agregar un caso nuevo = agregar una fila al CSV, sin tocar código.

Columnas del CSV:
    usuario, clave, debe_funcionar, descripcion
"""
import pytest

from pages.inventory_page import InventoryPage
from utils.datos import leer_csv_login
from utils.logger import logger

# Cargar datos del CSV al nivel del módulo
CASOS_LOGIN = leer_csv_login("datos/login.csv")


@pytest.mark.login
@pytest.mark.parametrize(
    "usuario, clave, debe_funcionar, descripcion",
    CASOS_LOGIN,
    ids=[c[3] for c in CASOS_LOGIN],  # usar la descripción como id del test
)
def test_login_parametrizado_csv(
    driver, usuario, clave, debe_funcionar, descripcion, request
):
    """Login parametrizado: valida todos los casos del CSV en un solo test."""
    from pages.login_page import LoginPage
    logger.info("Login CSV: caso '%s' (usuario=%s)", descripcion, usuario)

    login_page = LoginPage(driver)
    login_page.abrir().login_completo(usuario, clave)
    request.node.page_url = driver.current_url

    if debe_funcionar:
        inventory_page = InventoryPage(driver)
        assert inventory_page.esta_en_pagina_inventario(), \
            f"Caso '{descripcion}': debería redirigir a inventory.html"
    else:
        assert login_page.esta_error_visible(), \
            f"Caso '{descripcion}': debería mostrar mensaje de error"
