# tests/test_login_faker.py

import pytest
from faker import Faker
from pages.login_page import LoginPage


# Inicializar Faker con locale en espanol
fake = Faker('es_ES')


@pytest.mark.login
def test_login_faker_usuario_aleatorio(driver):
    """
    Test que intenta login con datos generados aleatoriamente por Faker.
    Como son credenciales inexistentes, el login deberia fallar y mostrar error.

    Este test es util para:
    - Probar que el sistema rechaza credenciales no registradas
    - Detectar bugs con caracteres especiales (acentos, Unicode)
    - Simular intentos de acceso no autorizado
    """
    usuario_aleatorio = fake.user_name()
    clave_aleatoria = fake.password(length=10)

    login_page = LoginPage(driver)
    login_page.abrir().login_completo(usuario_aleatorio, clave_aleatoria)

    # Credenciales Faker NUNCA seran validas en SauceDemo
    assert login_page.esta_error_visible(), \
        f"Login con Faker ({usuario_aleatorio}) deberia mostrar error"


@pytest.mark.login
def test_login_faker_email_como_usuario(driver):
    """
    Test que usa un email generado por Faker como nombre de usuario.
    Verifica que el sistema no se rompe con formato email en el campo usuario.
    """
    email_aleatorio = fake.email()

    login_page = LoginPage(driver)
    login_page.abrir().login_completo(email_aleatorio, fake.password())

    assert login_page.esta_error_visible(), \
        f"Login con email Faker ({email_aleatorio}) deberia mostrar error"


@pytest.mark.login
def test_login_faker_caracteres_especiales(driver):
    """
    Test que intenta login con caracteres especiales y acentos.
    Busca detectar bugs de encoding o inyecciones.
    """
    # Nombres con acentos y caracteres unicode
    usuarios_especiales = [
        fake.first_name() + " " + fake.last_name(),  # Nombre con espacios
        "usuario<script>",  # Intento de XSS
        "usuario'OR'1'='1",  # Intento de SQL injection
    ]

    for usuario in usuarios_especiales:
        login_page = LoginPage(driver)
        login_page.abrir().login_completo(usuario, fake.password())

        assert login_page.esta_error_visible(), \
            f"Login con '{usuario}' deberia mostrar error y no crashear"
