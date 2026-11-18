"""
tests_api/test_create_user_api.py — POST crear usuarios en ReqRes (Clase 11).

Crea un usuario por cada combinación de datos (parametrizado) y valida:
  - Status 201 Created.
  - Estructura (id + createdAt).
  - Contenido (nombre y trabajo coinciden, createdAt incluye el año actual).
"""
import requests
import pytest
from datetime import datetime

BASE_URL = "https://reqres.in"

pytestmark = pytest.mark.api

# Datos parametrizados: (nombre, trabajo)
CASOS_CREAR = [
    ("Matias QA", "tester"),
    ("Silvia PO", "product owner"),
    ("Juan Dev", "developer"),
    ("Ana Design", "designer"),
]


@pytest.mark.parametrize("nombre, trabajo", CASOS_CREAR)
def test_create_user_api(nombre, trabajo, request):
    """POST /api/users — crea un usuario y valida la respuesta."""
    payload = {"name": nombre, "job": trabajo}

    response = requests.post(f"{BASE_URL}/api/users", json=payload, timeout=10)
    request.node.page_url = response.url

    # Nivel 1: Status code — 201 Created
    assert response.status_code == 201

    # Nivel 3: Estructura JSON
    data = response.json()
    assert "id" in data, "No se generó id para el usuario"
    assert "createdAt" in data, "No se generó createdAt"

    # Nivel 4: Contenido — el nombre y trabajo coinciden
    assert data["name"] == nombre
    assert data["job"] == trabajo

    # Validar que createdAt incluya el año actual
    anio_actual = str(datetime.now().year)
    assert anio_actual in data["createdAt"], \
        f"createdAt no contiene el año actual ({anio_actual}): {data['createdAt']}"
