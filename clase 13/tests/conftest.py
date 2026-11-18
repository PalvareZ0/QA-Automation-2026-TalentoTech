import pytest
import os
from datetime import datetime

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Si el test falla durante la ejecución (call phase)
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            # Crear carpeta si no existe
            if not os.path.exists('reports/screenshots'):
                os.makedirs('reports/screenshots')
            
            # Nombre del archivo con fecha y nombre del test
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name
            screenshot_path = f"reports/screenshots/{test_name}_{timestamp}.png"
            
            # Guardar captura
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Captura de fallo guardada en: {screenshot_path}")