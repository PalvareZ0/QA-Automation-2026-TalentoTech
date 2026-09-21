import pytest
from calculadora import sumar, restar, multiplicar, dividir

# --- FIXTURES ---

@pytest.fixture
def numeros_enteros():
    """Prepara dos enteros comunes."""
    return 20, 5

@pytest.fixture
def numeros_decimales():
    """Prepara dos decimales para probar precisión."""
    return 0.1, 0.2