from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def agregar_primer_producto_al_carrito(driver):
    """Hace clic en el primer producto y espera explícitamente al badge."""
    # Buscamos el botón del primer producto
    driver.find_element(By.XPATH, "(//button[contains(@id, 'add-to-cart')])[1]").click()
    
    # ESPERA EXPLÍCITA: Esperamos hasta 10s a que el badge del carrito sea visible
    badge = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    return badge.text

def ir_al_carrito(driver):
    """Navega a la página del carrito y espera que cargue."""
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    # Esperamos explícitamente a que aparezca un item en el carrito
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "cart_item"))
    )