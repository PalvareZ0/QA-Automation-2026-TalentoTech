"""
tests/test_login_faker.py — Login con datos aleatorios generados por Faker (Clase 10).

Estos tests NO validan login exitoso (los datos Faker no existen en SauceDemo).
Sirven para:
  - Probar que el sistema rechaza credenciales no registradas.
  - Detectar bugs con caracteres especiales (acentos, Unicode).
  - Simular intentos de acceso no autorizado.
"""
import pytest
from faker import Faker

from pages.login_page import LoginPage
from utils.logger import logger

# Faker con locale español
fake = Faker('es_ES')


@pytest.mark.login
def test_login_faker_usuario_aleatorio(driver, request):
    """Login con usuario aleatorio de Faker debe mostrar error."""
    usuario_aleatorio = fake.user_name()
    clave_aleatoria = fake.password(length=10)

    logger.info("Faker: probando usuario aleatorio '%s'", usuario_aleatorio)
    login_page = LoginPage(driver)
    login_page.abrir().login_completo(usuario_aleatorio, clave_aleatoria)
    request.node.page_url = driver.current_url

    assert login_page.esta_error_visible(), \
        f"Login con Faker ({usuario_aleatorio}) debería mostrar error"


@pytest.mark.login
def test_login_faker_email_como_usuario(driver, request):
    """Login con email Faker como usuario debe mostrar error (no romper)."""
    email_aleatorio = fake.email()

    login_page = LoginPage(driver)
    login_page.abrir().login_completo(email_aleatorio, fake.password())
    request.node.page_url = driver.current_url

    assert login_page.esta_error_visible(), \
        f"Login con email Faker ({email_aleatorio}) debería mostrar error"


@pytest.mark.login
def test_login_faker_caracteres_especiales(driver, request):
    """Login con acentos, espacios y caracteres de intento de inyección."""
    usuarios_especiales = [
        fake.first_name() + " " + fake.last_name(),  # Nombre con espacios
        "usuario<script>",                            # Intento de XSS
        "usuario'OR'1'='1",                          # Intento de SQL injection
    ]

    for usuario in usuarios_especiales:
        login_page = LoginPage(driver)
        login_page.abrir().login_completo(usuario, fake.password())
        request.node.page_url = driver.current_url

        assert login_page.esta_error_visible(), \
            f"Login con '{usuario}' debería mostrar error y no crashear"
