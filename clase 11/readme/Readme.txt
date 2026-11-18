🚀 Pre-Entrega: QA Automation Testing - SauceDemo
Este proyecto automatiza pruebas funcionales E2E (End-to-End) en el sitio web SauceDemo (https://www.saucedemo.com/), validando el flujo crítico de login, navegación de inventario y carrito de compras.

🛠️ Tecnologías Utilizadas
Python 3.x: Lenguaje principal.
Selenium WebDriver 4.x: Automatización del navegador.
Pytest: Framework de testing y generación de reportes.
WebDriver Manager: Gestión automática de drivers.
Git/GitHub: Control de versiones.
📁 Estructura del Proyecto
tests/: Contiene los casos de prueba (test_saucedemo.py) y el conftest.py para capturas de fallos.
utils/: Funciones auxiliares (configuración del driver y acciones del carrito).
reports/: Se generan los reportes HTML y capturas de pantalla al fallar.
datos/: Reservado para data driven testing futuro.
⚙️ Instalación de Dependencias
Clonar el repositorio: git clone <URL>
Crear entorno virtual (recomendado): python -m venv venv y activarlo.
Instalar dependencias:
pip install -r requirements.txt
💻 Cómo Ejecutar las Pruebas
Ejecuta el siguiente comando desde la raíz del proyecto para correr los tests y generar el reporte HTML:
pytest tests/test_saucedemo.py -v --html=reports/reporte.html
abrir reports/reporte.html en tu navegador para ver los resultados detallados y las capturas de pantalla en caso de fallos.

Ejecutar localmente y generar el Reporte

Antes de subir a GitHub, asegúratese de que todo funcione:

1. En tu terminal, en la raíz del proyecto, ejecuta:
   ```bash
   pytest tests/test_saucedemo.py -v --html=reports/reporte.html

   - Verificar que en la consola salgan 2 passed

