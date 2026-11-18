import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importamos nuestras funciones auxiliares
from utils.driver_setup import iniciar_driver
from utils.cart_actions import agregar_primer_producto_al_carrito, ir_al_carrito

@pytest.fixture
def driver():
    """Fixture que inicializa el driver antes de cada test y lo cierra después."""
    driver = iniciar_driver()
    yield driver
    driver.quit()

def test_login_y_navegacion(driver):
    """Caso de Prueba 1: Login y verificación del catálogo."""
    # 1. Abrir login
    driver.get("https://www.saucedemo.com/")
    
    # 2. Completar credenciales
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # 3. Validar login exitoso (Esperamos explícitamente a que cargue el inventario)
    WebDriverWait(driver, 10).until(
        EC.url_contains("/inventory.html")
    )
    assert "Swag Labs" in driver.title
    
    # 4. Verificar catálogo (Título y Productos)
    titulo = driver.find_element(By.CSS_SELECTOR, ".title").text
    assert titulo == "Products", f"Se esperaba 'Products', pero se obtuvo {titulo}"
    
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0, "No hay productos visibles en el inventario"
    
    # Mostrar nombre y precio del primer producto en consola
    primer_nombre = productos[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    primer_precio = productos[0].find_element(By.CLASS_NAME, "inventory_item_price").text
    print(f"\n✅ Primer producto encontrado: {primer_nombre} - {primer_precio}")

def test_interaccion_carrito(driver):
    """Caso de Prueba 2: Interacción con productos y carrito."""
    # Pre-requisito: Estar logueado (hacemos el login rápido)
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))
    
    # 5. Agregar primer producto usando nuestra función auxiliar
    badge_text = agregar_primer_producto_al_carrito(driver)
    
    # 6. Confirmar que el badge dice "1"
    assert badge_text == "1", f"El carrito debería mostrar 1, pero muestra {badge_text}"
    
    # 7. Ir al carrito y verificar producto
    ir_al_carrito(driver)
    
    items_carrito = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items_carrito) == 1, "Debería haber exactamente 1 producto en el carrito"
    
    print("\n✅ Test OK: Producto agregado y verificado en carrito correctamente.")