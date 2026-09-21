from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def iniciar_driver():
    """Configura y devuelve una instancia del WebDriver de Chrome."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Inicializar el driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Espera implícita como red de seguridad global (5 seg)
    driver.implicitly_wait(5)
    return driver