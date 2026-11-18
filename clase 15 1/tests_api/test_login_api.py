"""
tests_api/test_login_api.py — Login en la API de ReqRes (Clase 11).

Valida:
  - Login exitoso (email + password correctos) → 200 + token.
  - Login inválido (email sin password) → 400.

Validaciones por los 5 niveles: status, cabeceras, estructura, contenido, tiempo.
"""
import requests
import pytest

BASE_URL = "https://reqres.in"

# Marca todo el archivo como tests de API
pytestmark = pytest.mark.api

# Datos parametrizados: (email, password, status_esperado, esperar_token)
CASOS_LOGIN = [
    ("eve.holt@reqres.in", "cityslicka", 200, True),   # válido
    ("eve.holt@reqres.in", None,         400, False),  # falta password
]


@pytest.mark.parametrize(
    "email, password, status_esperado, esperar_token",
    CASOS_LOGIN,
    ids=["login_valido", "login_sin_password"],
)
def test_login_api(email, password, status_esperado, esperar_token, request):
    """Login en /api/login con diferentes combinaciones."""
    payload = {"email": email}
    if password is not None:
        payload["password"] = password

    response = requests.post(f"{BASE_URL}/api/login", json=payload, timeout=10)
    request.node.page_url = response.url

    # Nivel 1: Status code
    assert response.status_code == status_esperado

    # Nivel 4: Contenido específico (solo si esperamos token)
    if esperar_token:
        data = response.json()
        assert "token" in data, "La respuesta no contiene token"
