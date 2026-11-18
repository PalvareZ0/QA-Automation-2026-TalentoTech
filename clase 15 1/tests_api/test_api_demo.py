"""
tests_api/test_api_demo.py — Tests API de demostración (Clase 13).

Muestra capacidades avanzadas del framework de observabilidad:
  - Soft-asserts con pytest-check (no cortan en el primer fallo).
  - Logging de cada paso.
  - Retry automático para tests flaky (pytest-rerunfailures).
"""
import requests
import pytest
import pytest_check as check

from utils.logger import logger

BASE = "https://jsonplaceholder.typicode.com"


@pytest.mark.api
def test_get_usuario_con_soft_asserts(request):
    """GET /users/1 — valida TODO con soft-asserts (no corta en el primer fallo)."""
    logger.info("GET %s/users/1", BASE)
    resp = requests.get(f"{BASE}/users/1", timeout=10)
    request.node.page_url = resp.url

    # ✅ Verifica TODO aunque algo falle: el reporte lista cada validación
    check.equal(resp.status_code, 200, "El status no es 200")
    check.is_true(
        "application/json" in resp.headers.get("Content-Type", ""),
        "La respuesta no es JSON",
    )
    data = resp.json()
    check.is_in("id", data, "Falta la clave 'id'")
    check.equal(data.get("id"), 1, "El id no es 1")
    check.is_in("email", data, "Falta la clave 'email'")
    elapsed = resp.elapsed.total_seconds()
    check.is_true(elapsed < 2, f"Demoró {elapsed:.2f}s (> 2s)")
    logger.info("Soft-asserts completados (6 validaciones)")


@pytest.mark.api
def test_post_crea_recurso(request):
    """POST /posts — crea un recurso y valida la respuesta."""
    payload = {"title": "QA-145 Reportes y Logging", "body": "Demo", "userId": 1}
    logger.info("POST %s/posts con payload: %s", BASE, payload)

    resp = requests.post(f"{BASE}/posts", json=payload, timeout=10)
    request.node.page_url = resp.url

    assert resp.status_code == 201, f"Status inesperado: {resp.status_code}"
    data = resp.json()
    assert data["title"] == payload["title"]
    logger.info("Recurso creado con id: %s", data.get("id"))


_intentos = {"n": 0}


@pytest.mark.api
@pytest.mark.flaky(reruns=2, reruns_delay=1)  # reintenta hasta 2 veces
def test_demo_retry_flaky():
    """
    Demuestra el mecanismo de retry para tests inestables (flaky).
    Falla en el primer intento y pasa en el segundo, mostrando 'Reruns'
    en el reporte. Los retries son solo para tests inestables por red/
    infraestructura, nunca para bugs de código reales.
    """
    _intentos["n"] += 1
    logger.info("Intento número %s de test_demo_retry_flaky", _intentos["n"])
    assert _intentos["n"] >= 2, "Falla a propósito en el 1er intento"
