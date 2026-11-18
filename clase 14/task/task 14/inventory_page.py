"""
pages/inventory_page.py — Page Object del inventario de SauceDemo
Nota técnica: los clics de productos esperan el cambio real del badge del
carrito; si el clic nativo no tuvo efecto (página sin foco en headless),
se repite por JS.
"""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ESPERA_MAX = 10  # segundos (esperas explícitas)


class InventoryPage:
    # 📍 Locators
    _TITULO = (By.CSS_SELECTOR, ".title")
    _CONTADOR_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def __init__(self, driver):
        self.driver = driver

    # ---- Acciones ----
    def agregar_producto(self, nombre: str):
        """Agrega un producto al carrito por su nombre (ej: 'Sauce Labs Backpack').
        Verifica que el badge del carrito cambie; si el clic nativo no tuvo
        efecto, lo repite por JS."""
        slug = nombre.strip().lower().replace(" ", "-")
        locator = (By.ID, f"add-to-cart-{slug}")
        WebDriverWait(self.driver, ESPERA_MAX).until(
            EC.element_to_be_clickable(locator)
        )
        boton = self.driver.find_element(*locator)
        antes = self.contador_carrito()
        try:
            boton.click()
            WebDriverWait(self.driver, 3).until(
                lambda d: self.contador_carrito() != antes
            )
        except TimeoutException:
            self.driver.execute_script("arguments[0].click();", boton)
            WebDriverWait(self.driver, ESPERA_MAX).until(
                lambda d: self.contador_carrito() != antes
            )
        return self

    # ---- Helpers de consulta ----
    def titulo(self) -> str:
        """Título visible del inventario ('Products')."""
        return self.driver.find_element(*self._TITULO).text

    def contador_carrito(self) -> str:
        """Número que muestra el badge del carrito ('0' si no hay productos)."""
        return self._valor_badge() or "0"

    def _valor_badge(self) -> str:
        """Texto del badge actual, o '' si todavía no existe.
        Consulta OPCIONAL: desactiva momentáneamente la espera implícita
        para que no se frene 5s cuando el badge aún no está en la página."""
        self.driver.implicitly_wait(0)
        try:
            elementos = self.driver.find_elements(*self._CONTADOR_CARRITO)
            return elementos[0].text if elementos else ""
        finally:
            self.driver.implicitly_wait(5)
