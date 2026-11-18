"""
features/steps/operaciones_steps.py — Conectores del ejemplo de lógica pura
(Ejemplo 1 de la clase: BDD sin navegador, sobre una función de utils/)
"""
from behave import then, when

from utils.logger import logger
from utils.operaciones import multiplicar


@when('multiplico {a:d} y {b:d}')
def step_multiplicar(context, a, b):
    """Ejecuta la multiplicación y guarda el resultado en context."""
    context.resultado = multiplicar(a, b)
    logger.info("BDD: multiplicar(%s, %s)", a, b)


@then('obtengo {esperado:d}')
def step_validar_producto(context, esperado):
    """Verifica que el resultado coincide con lo esperado."""
    assert context.resultado == esperado, (
        f"Esperaba {esperado}, obtuve {context.resultado}"
    )
