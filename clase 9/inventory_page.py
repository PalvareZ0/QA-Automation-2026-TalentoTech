# pages/inventory_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    """Page Object para la pagina de inventario/productos de SauceDemo."""

    # LOCATORS (privados y centralizados)
    _TITLE = (By.CLASS_NAME, "title")
    _PRODUCTS = (By.CLASS_NAME, "inventory_item")
    _PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _ADD_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Metodos de lectura (obtener informacion) ---

    def obtener_titulo(self) -> str:
        """Obtiene el titulo de la pagina de inventario."""
        return self.driver.find_element(*self._TITLE).text

    def obtener_productos(self) -> list:
        """Obtiene la lista de elementos producto disponibles."""
        return self.driver.find_elements(*self._PRODUCTS)

    def obtener_cantidad_productos(self) -> int:
        """Obtiene la cantidad de productos visibles."""
        return len(self.driver.find_elements(*self._PRODUCTS))

    def obtener_nombres_productos(self) -> list:
        """Obtiene los nombres de todos los productos."""
        elementos = self.driver.find_elements(*self._PRODUCT_NAMES)
        return [e.text for e in elementos]

    def obtener_primer_producto_info(self) -> dict:
        """Obtiene nombre y precio del primer producto."""
        productos = self.driver.find_elements(*self._PRODUCTS)
        if productos:
            nombre = productos[0].find_element(By.CLASS_NAME, "inventory_item_name").text
            precio = productos[0].find_element(By.CLASS_NAME, "inventory_item_price").text
            return {"nombre": nombre, "precio": precio}
        return {}

    # --- Metodos de accion ---

    def agregar_primer_producto(self):
        """Anade el primer producto disponible al carrito."""
        primer_boton = self.driver.find_elements(*self._ADD_BUTTONS)[0]
        primer_boton.click()
        return self

    def obtener_contador_carrito(self) -> int:
        """Obtiene el numero de productos en el carrito (badge)."""
        try:
            badge = self.driver.find_element(*self._CART_BADGE)
            return int(badge.text)
        except:
            return 0

    # --- Navegacion a otras paginas (retornan Page Objects) ---

    def ir_al_carrito(self):
        """Navega a la pagina del carrito y retorna CartPage."""
        self.driver.find_element(*self._CART_LINK).click()
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    def hacer_logout(self):
        """Cierra la sesion y retorna LoginPage."""
        self.driver.find_element(*self._MENU_BUTTON).click()
        logout_link = self.wait.until(
            EC.element_to_be_clickable(self._LOGOUT_LINK)
        )
        logout_link.click()
        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    # --- Verificaciones ---

    def esta_en_pagina_inventario(self) -> bool:
        """Verifica si estamos en la pagina de inventario."""
        return "/inventory.html" in self.driver.current_url
