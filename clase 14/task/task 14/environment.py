"""
features/environment.py — Hooks globales de Behave (QA-158, Tarea 4)
El "backstage" de la suite BDD: prepara y limpia todo lo que los steps
no deberían tocar (navegador, logs, capturas de fallos).
"""
import os
import pathlib
from datetime import datetime

from selenium import webdriver

from utils.logger import logger

# 📁 Carpeta de capturas (se crea sola)
SCREEN_DIR = pathlib.Path("reports/screens")
SCREEN_DIR.mkdir(parents=True, exist_ok=True)


def before_all(context):
    """Arranca el navegador UNA sola vez para toda la suite BDD."""
    options = webdriver.ChromeOptions()
    # Headless por defecto (ideal para CI/CD). Para VER el navegador:
    #   HEADLESS=0 behave
    if os.getenv("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(5)   # evita sleeps fijos
    context.driver.maximize_window()
    logger.info("BDD: suite iniciada (navegador abierto)")


def before_scenario(context, scenario):
    """Resetea el estado del navegador entre escenarios (SauceDemo guarda
    la sesión en localStorage) y registra el inicio en el log."""
    driver = getattr(context, "driver", None)
    if driver is not None:
        try:
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
        except Exception:
            pass  # primera vez (página en blanco): nada que limpiar
    logger.info("BDD: ▶ escenario: %s", scenario.name)


def after_step(context, step):
    """📸 Captura automática si un paso falla (evidencia para el reporte)."""
    if step.status == "failed" and hasattr(context, "driver"):
        marca = datetime.now().strftime("%H%M%S")
        nombre = step.name.replace('"', "").replace(" ", "_")[:50] or "paso"
        archivo = SCREEN_DIR / f"bdd_{nombre}_{marca}.png"
        try:
            context.driver.save_screenshot(str(archivo))
            logger.error("BDD: captura de fallo guardada en %s", archivo)
        except Exception:
            pass  # navegador caído: no rompemos la evidencia


def after_scenario(context, scenario):
    """Registra el resultado de cada escenario en el log."""
    logger.info("BDD: escenario '%s' terminó → %s", scenario.name, scenario.status)


def after_all(context):
    """Cierra el navegador y libera recursos (sin procesos huérfanos)."""
    if hasattr(context, "driver"):
        context.driver.quit()
    logger.info("BDD: suite finalizada (navegador cerrado)")
