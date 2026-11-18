# pages/cart_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Page Object para la pagina del carrito de compras de SauceDemo."""

    # LOCATORS (privados y centralizados)
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Verificar que estamos en la pagina correcta
        self.wait.until(EC.url_contains("cart.html"))

    # --- Metodos de lectura ---

    def obtener_productos_en_carrito(self) -> list:
        """Obtiene la lista de elementos producto en el carrito."""
        return self.driver.find_elements(*self._CART_ITEMS)

    def obtener_cantidad_productos(self) -> int:
        """Obtiene la cantidad de productos en el carrito."""
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def obtener_nombres_productos(self) -> list:
        """Obtiene los nombres de todos los productos en el carrito."""
        elementos_nombre = self.driver.find_elements(*self._ITEM_NAMES)
        return [elemento.text for elemento in elementos_nombre]

    def contiene_producto(self, nombre_producto: str) -> bool:
        """Verifica si un producto especifico esta en el carrito."""
        nombres = self.obtener_nombres_productos()
        return nombre_producto in nombres

    # --- Navegacion ---

    def continuar_comprando(self):
        """Regresa a la pagina de inventario y retorna InventoryPage."""
        self.driver.find_element(*self._CONTINUE_SHOPPING).click()
        from pages.inventory_page import InventoryPage
        return InventoryPage(self.driver)

    def proceder_checkout(self):
        """Inicia el proceso de checkout."""
        self.driver.find_element(*self._CHECKOUT_BUTTON).click()
        return self
