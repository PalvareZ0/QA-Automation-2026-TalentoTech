import pytest

BASE_JPH = "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="module")
def posts_url():
    """URL base para la colección de posts"""
    return f"{BASE_JPH}/posts"

@pytest.fixture(scope="module")
def post_by_id_url():
    """Función que genera URLs específicas por ID"""
    def _get_url(post_id):
        return f"{BASE_JPH}/posts/{post_id}"
    return _get_url