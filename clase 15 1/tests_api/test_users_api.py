"""
tests_api/test_users_api.py — GET de usuarios en ReqRes (Clase 11).

Valida:
  - Estructura de cada usuario (claves obligatorias).
  - Contenido (IDs positivos, emails válidos, nombres no vacíos).
  - Formato del avatar (.jpg).
"""
import requests
import pytest

BASE_URL = "https://reqres.in"

pytestmark = pytest.mark.api


def test_get_users_structure(request):
    """GET /api/users?page=1 — estructura de cada usuario."""
    response = requests.get(f"{BASE_URL}/api/users?page=1", timeout=10)
    request.node.page_url = response.url

    # Nivel 1: Status code
    assert response.status_code == 200

    # Nivel 3: Estructura
    data = response.json()
    assert "data" in data, "No existe el campo 'data' en la respuesta"

    users = data["data"]
    assert len(users) > 0, "La lista de usuarios está vacía"

    claves_obligatorias = {"id", "email", "first_name", "last_name"}
    for user in users:
        claves_usuario = set(user.keys())
        assert claves_obligatorias <= claves_usuario, \
            f"Al usuario le faltan claves: {claves_obligatorias - claves_usuario}"
        # El avatar debe terminar en .jpg
        assert user["avatar"].endswith(".jpg"), \
            f"El avatar de {user['first_name']} no termina en .jpg: {user['avatar']}"


def test_get_users_content(request):
    """GET /api/users?page=1 — validaciones de contenido (Nivel 4)."""
    response = requests.get(f"{BASE_URL}/api/users?page=1", timeout=10)
    request.node.page_url = response.url
    data = response.json()
    users = data["data"]

    for user in users:
        assert user["id"] > 0, f"ID inválido: {user['id']}"
        assert "@" in user["email"], f"Email inválido: {user['email']}"
        assert len(user["first_name"]) > 0, "first_name vacío"
        assert len(user["last_name"]) > 0, "last_name vacío"
