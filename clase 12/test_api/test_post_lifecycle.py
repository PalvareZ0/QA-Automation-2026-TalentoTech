import requests
import pytest
from faker import Faker

BASE_URL = "https://jsonplaceholder.typicode.com"

# Marcar todo el archivo como e2e y api
pytestmark = [pytest.mark.api, pytest.mark.e2e]

# --- Fixture: crea un post y devuelve sus datos ---
@pytest.fixture(scope="module")
def created_post():
    """Crea un post con Faker y devuelve sus datos para otros tests"""
    fake = Faker("es_ES")
    payload = {
        "title": fake.sentence(nb_words=5),
        "body": fake.paragraph(nb_sentences=3),
        "userId": 1
    }

    response = requests.post(f"{BASE_URL}/posts", json=payload)

    # Nivel 1: Status code — 201 Created
    assert response.status_code == 201

    # Nivel 3: Estructura — debe tener id, title, body, userId
    data = response.json()
    assert "id" in data, "No se generó id para el post"

    return data


# --- Test 1: Verificar que el post fue creado correctamente ---
def test_post_created(created_post):
    """Valida que el post creado tenga la estructura correcta"""
    # Nivel 3: Estructura — claves obligatorias
    claves_obligatorias = {"id", "title", "body", "userId"}
    assert claves_obligatorias <= set(created_post.keys()), \
        f"Faltan claves: {claves_obligatorias - set(created_post.keys())}"

    # Nivel 4: Contenido — ID positivo, título no vacío
    assert created_post["id"] > 0
    assert len(created_post["title"]) > 0
    assert len(created_post["body"]) > 0


# --- Test 2: PATCH — actualizar título del post creado ---
def test_patch_created_post(created_post):
    """Actualiza solo el título del post creado con PATCH"""
    post_id = created_post["id"]
    nuevo_titulo = "Título actualizado por QA"

    patch_payload = {"title": nuevo_titulo}
    response = requests.patch(
        f"{BASE_URL}/posts/{post_id}",
        json=patch_payload
    )

    # Nivel 1: Status code
    assert response.status_code == 200

    # Nivel 2: Cabeceras — debe devolver JSON
    assert "application/json" in response.headers.get("Content-Type", "")

    # Nivel 3: Estructura — mantener campos originales + actualizados
    body = response.json()
    claves_esperadas = {"id", "title", "body", "userId"}
    assert claves_esperadas <= set(body.keys()), \
        f"PATCH eliminó campos: {claves_esperadas - set(body.keys())}"

    # Nivel 4: Contenido — título actualizado, resto intacto
    assert body["title"] == nuevo_titulo, "PATCH no actualizó el título"
    assert "body" in body and body["body"] is not None, \
        "PATCH no preservó el campo body"

    # Nivel 5: Performance — PATCH debe ser rápido
    assert response.elapsed.total_seconds() < 1.5, "PATCH demasiado lento"


# --- Test 3: DELETE — eliminar el post creado ---
def test_delete_created_post(created_post):
    """Elimina el post creado y verifica la respuesta"""
    post_id = created_post["id"]

    response = requests.delete(f"{BASE_URL}/posts/{post_id}")

    # Nivel 1: Status code — 200 (JSONPlaceholder) o 204
    assert response.status_code in [200, 204], \
        f"DELETE devolvió {response.status_code}, esperado 200 o 204"

    # Nivel 2: Cabeceras (si es 204, no hay contenido)
    if response.status_code == 204:
        assert response.headers.get("Content-Length", "0") == "0", \
            "204 no debe tener contenido"

    # Nivel 3: Estructura — cuerpo vacío o con campos null
    if response.status_code == 200 and response.text:
        body = response.json()
        assert body == {} or all(v is None for v in body.values()), \
            "DELETE debe vaciar el recurso"

    # Nivel 5: Performance — DELETE debe ser la operación más rápida
    assert response.elapsed.total_seconds() < 1.0, "DELETE demasiado lento"