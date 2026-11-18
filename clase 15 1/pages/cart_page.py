"""
pages/cart_page.py — Page Object del carrito de compras de SauceDemo.

Encapsula selectores y acciones de la página /cart.html. Permite leer los
productos agregados, verificar si un producto específico está en el carrito,
continuar comprando o iniciar el checkout.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ESPERA_MAX = 10  # segundos


class CartPage:
    """Page Object para la página del carrito de compras de SauceDemo."""

    # 📍 Locators (privados y centralizados)
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ESPERA_MAX)
        # Verificar que estamos en la página correcta
        self.wait.until(EC.url_contains("cart.html"))

    # ---- Métodos de lectura ----

    def obtener_productos_en_carrito(self) -> list:
        """Lista de elementos producto en el carrito."""
        return self.driver.find_elements(*self._CART_ITEMS)

    def obtener_cantidad_productos(self) -> int:
        """Cantidad de productos en el carrito."""
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def obtener_nombres_productos(self) -> list:
        """Nombres de todos los productos en el carrito."""
        elementos = self.driver.find_elements(*self._ITEM_NAMES)
        return [e.text for e in elementos]

    def contiene_producto(self, nombre_producto: str) -> bool:
        """True si el producto indicado está en el carrito."""
        return nombre_producto in self.obtener_nombres_productos()

    # ---- Navegación ----

    def continuar_comprando(self):
        """Regresa a la página de inventario y retorna InventoryPage."""
        self.driver.find_element(*self._CONTINUE_SHOPPING).click()
        from pages.inventory_page import InventoryPage
        return InventoryPage(self.driver)

    def proceder_checkout(self):
        """Inicia el proceso de checkout."""
        self.driver.find_element(*self._CHECKOUT_BUTTON).click()
        return self
