"""
tests_api/conftest.py — Fixtures comunes para tests de API (Clase 12).

Centraliza las URLs base para que sea fácil cambiar entre entornos
(dev/staging/prod) y evitar duplicación.
"""
import pytest

BASE_JPH = "https://jsonplaceholder.typicode.com"
BASE_REQRES = "https://reqres.in"


@pytest.fixture(scope="module")
def posts_url():
    """URL base para la colección de posts (JSONPlaceholder)."""
    return f"{BASE_JPH}/posts"


@pytest.fixture(scope="module")
def post_by_id_url():
    """Función que genera URLs específicas por ID."""
    def _get_url(post_id):
        return f"{BASE_JPH}/posts/{post_id}"
    return _get_url


@pytest.fixture(scope="module")
def reqres_base():
    """URL base de la API ReqRes (usuarios, login)."""
    return BASE_REQRES
