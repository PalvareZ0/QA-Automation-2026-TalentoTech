import requests
import pytest

BASE_URL = "https://reqres.in"

pytestmark = pytest.mark.api

def test_get_users_structure():
    # Hacer GET a la página 1
    response = requests.get(f"{BASE_URL}/api/users?page=1")

    # Nivel 1: Status code
    assert response.status_code == 200

    # Nivel 3: Estructura JSON — verificar que exista la lista de usuarios
    data = response.json()
    assert "data" in data, "No existe el campo 'data' en la respuesta"

    users = data["data"]
    assert len(users) > 0, "La lista de usuarios está vacía"

    # Claves obligatorias que cada usuario debe tener
    claves_obligatorias = {"id", "email", "first_name", "last_name"}

    for user in users:
        # Verificar que el usuario tenga todas las claves obligatorias
        claves_usuario = set(user.keys())
        assert claves_obligatorias <= claves_usuario, \
            f"Al usuario le faltan claves: {claves_obligatorias - claves_usuario}"

        # Extra: validar que el avatar termine en .jpg
        assert user["avatar"].endswith(".jpg"), \
            f"El avatar de {user['first_name']} no termina en .jpg: {user['avatar']}"

def test_get_users_content():
    # Validaciones de contenido (Nivel 4)
    response = requests.get(f"{BASE_URL}/api/users?page=1")
    data = response.json()
    users = data["data"]

    for user in users:
        # IDs positivos
        assert user["id"] > 0, f"ID inválido: {user['id']}"
        # Email con formato válido (contiene @)
        assert "@" in user["email"], f"Email inválido: {user['email']}"
        # Nombres no vacíos
        assert len(user["first_name"]) > 0, "first_name vacío"
        assert len(user["last_name"]) > 0, "last_name vacío"