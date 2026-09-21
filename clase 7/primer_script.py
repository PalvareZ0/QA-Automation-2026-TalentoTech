from selenium import webdriver

driver = webdriver.Chrome() # Abre Chrome automáticamente
try:
    driver.get('https://www.saucedemo.com')
    print('Título:', driver.title)
    assert driver.title == 'Swag Labs'
    print("¡Conexión exitosa!")
finally:
    driver.quit() # Siempre cierra el navegador

    ###

    driver.implicitly_wait(5) # Espera hasta 5s a que los elementos aparezcan

    ###

    from selenium.webdriver.common.by import By

driver.find_element(By.ID, "user-name")
driver.find_element(By.CSS_SELECTOR, ".inventory_item")
driver.find_element(By.XPATH, "//button[text()='Add to cart']")

# Así se verá en la Clase 8 >
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.implicitly_wait(5)
    yield d
    d.quit()

def test_login_exitoso(driver):
    driver.get('https://www.saucedemo.com')
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    # ... resto del test

