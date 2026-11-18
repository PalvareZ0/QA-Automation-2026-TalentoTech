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
def test_create_user_api(nombre, trabajo):
    # Armar el payload
    payload = {"name": nombre, "job": trabajo}

    # Enviar POST
    response = requests.post(f"{BASE_URL}/api/users", json=payload)

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
    anio_actual = str(datetime.now().year)  # "2026"
    assert anio_actual in data["createdAt"], \
        f"createdAt no contiene el año actual ({anio_actual}): {data['createdAt']}"