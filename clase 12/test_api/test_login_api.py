import requests
import pytest

BASE_URL = "https://reqres.in"

# Marker para agrupar todos los tests de API
pytestmark = pytest.mark.api  # marca todo el archivo

# Datos parametrizados: (email, password, status_esperado, esperar_token)
CASOS_LOGIN = [
    # Caso válido: email + password correctos → 200 + token
    ("eve.holt@reqres.in", "cityslicka", 200, True),
    # Caso inválido: email sin password → 400
    ("eve.holt@reqres.in", None, 400, False),
]

@pytest.mark.parametrize(
    "email, password, status_esperado, esperar_token",
    CASOS_LOGIN
)
def test_login_api(email, password, status_esperado, esperar_token):
    # Armar el payload: si password es None, no lo incluimos
    payload = {"email": email}
    if password is not None:
        payload["password"] = password

    # Enviar POST al endpoint de login
    response = requests.post(f"{BASE_URL}/api/login", json=payload)

    # Nivel 1: Status code
    assert response.status_code == status_esperado

    # Nivel 4: Contenido específico (solo si esperamos token)
    if esperar_token:
        data = response.json()
        assert "token" in data, "La respuesta no contiene token"