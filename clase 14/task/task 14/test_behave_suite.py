"""
tests_behave/test_behave_suite.py — Wrapper: Behave ejecutado desde Pytest
(QA-158, Tarea 5)

Corre las historias BDD como si fueran tests de Pytest, generando reportes
JSON + HTML. Así TODO (tests Pytest + suite BDD) sale con un solo comando:

    pytest
"""
import pathlib
import subprocess
import sys

import pytest

REPORTS_DIR = pathlib.Path("reports")


def _ejecutar_behave(tags: str, json_salida: str, html_salida: str):
    """Corre Behave con los tags indicados y genera los reportes."""
    REPORTS_DIR.mkdir(exist_ok=True)
    return subprocess.run(
        [
            sys.executable, "-m", "behave",
            "features",
            "-t", tags,
            "-f", "json", "-o", str(REPORTS_DIR / json_salida),
            "-f", "html", "-o", str(REPORTS_DIR / html_salida),
            "-f", "pretty",
        ],
        check=False,
    )


@pytest.mark.bdd
def test_behave_smoke():
    """Suite BDD @smoke: login (demo para el cliente)."""
    resultado = _ejecutar_behave("@smoke", "behave_smoke.json", "behave_smoke.html")
    assert resultado.returncode == 0, (
        "La suite BDD @smoke falló — evidencia en reports/behave_smoke.html"
    )


@pytest.mark.bdd
def test_behave_regression():
    """Suite BDD @regression: carrito."""
    resultado = _ejecutar_behave(
        "@regression", "behave_regression.json", "behave_regression.html"
    )
    assert resultado.returncode == 0, (
        "La suite BDD @regression falló — evidencia en reports/behave_regression.html"
    )
