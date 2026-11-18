"""
pages/inventory_page.py — Page Object del inventario de SauceDemo.

Fusiona la versión robusta de la Clase 14 (clics por JS, espera del badge)
con los métodos extra de clases anteriores (titulo, productos, primer
producto, navegación a carrito y logout).

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
    """Page Object para la página de inventario/productos de SauceDemo."""

    # 📍 Locators (privados y centralizados)
    _TITULO = (By.CSS_SELECTOR, ".title")
    _PRODUCTS = (By.CLASS_NAME, "inventory_item")
    _PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _ADD_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    _CONTADOR_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ESPERA_MAX)

    # ---- Métodos de lectura (obtener información) ----

    def titulo(self) -> str:
        """Título visible del inventario ('Products')."""
        return self.driver.find_element(*self._TITULO).text

    def obtener_titulo(self) -> str:
        """Alias legible del título."""
        return self.titulo()

    def obtener_productos(self) -> list:
        """Lista de elementos producto visibles."""
        return self.driver.find_elements(*self._PRODUCTS)

    def obtener_cantidad_productos(self) -> int:
        """Cantidad de productos visibles en el inventario."""
        return len(self.driver.find_elements(*self._PRODUCTS))

    def obtener_nombres_productos(self) -> list:
        """Nombres de todos los productos visibles."""
        elementos = self.driver.find_elements(*self._PRODUCT_NAMES)
        return [e.text for e in elementos]

    def obtener_primer_producto_info(self) -> dict:
        """Nombre y precio del primer producto (o {} si no hay)."""
        productos = self.driver.find_elements(*self._PRODUCTS)
        if productos:
            nombre = productos[0].find_element(
                By.CLASS_NAME, "inventory_item_name"
            ).text
            precio = productos[0].find_element(
                By.CLASS_NAME, "inventory_item_price"
            ).text
            return {"nombre": nombre, "precio": precio}
        return {}

    # ---- Métodos de acción ----

    def agregar_producto(self, nombre: str):
        """Agrega un producto al carrito por su nombre (ej: 'Sauce Labs Backpack').
        Verifica que el badge del carrito cambie; si el clic nativo no tuvo
        efecto, lo repite por JS."""
        slug = nombre.strip().lower().replace(" ", "-")
        locator = (By.ID, f"add-to-cart-{slug}")
        self.wait.until(EC.element_to_be_clickable(locator))
        boton = self.driver.find_element(*locator)
        antes = self.contador_carrito()
        try:
            boton.click()
            WebDriverWait(self.driver, 5).until(
                lambda d: self.contador_carrito() != antes
            )
        except TimeoutException:
            # Reintento por JS (a veces el clic nativo no 'pega' en headless)
            self.driver.execute_script("arguments[0].click();", boton)
            WebDriverWait(self.driver, ESPERA_MAX).until(
                lambda d: self.contador_carrito() != antes
            )
        return self

    def agregar_producto_por_nombre(self, nombre: str):
        """Alias del método de arriba (compatibilidad con tests antiguos)."""
        return self.agregar_producto(nombre)

    def agregar_primer_producto(self):
        """Agrega el primer producto disponible al carrito."""
        primer_boton = self.driver.find_elements(*self._ADD_BUTTONS)[0]
        antes = self.contador_carrito()
        primer_boton.click()
        try:
            WebDriverWait(self.driver, 3).until(
                lambda d: self.contador_carrito() != antes
            )
        except TimeoutException:
            self.driver.execute_script("arguments[0].click();", primer_boton)
            WebDriverWait(self.driver, ESPERA_MAX).until(
                lambda d: self.contador_carrito() != antes
            )
        return self

    # ---- Helpers de consulta del carrito ----

    def contador_carrito(self) -> str:
        """Número que muestra el badge del carrito ('0' si no hay productos)."""
        return self._valor_badge() or "0"

    def obtener_contador_carrito(self) -> int:
        """Int del badge del carrito (0 si está vacío)."""
        try:
            return int(self.contador_carrito())
        except ValueError:
            return 0

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

    # ---- Navegación a otras páginas (retornan Page Objects) ----

    def ir_al_carrito(self):
        """Navega a la página del carrito y retorna CartPage."""
        self.driver.find_element(*self._CART_LINK).click()
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    def hacer_logout(self):
        """Cierra la sesión y retorna LoginPage."""
        self.driver.find_element(*self._MENU_BUTTON).click()
        logout_link = self.wait.until(
            EC.element_to_be_clickable(self._LOGOUT_LINK)
        )
        logout_link.click()
        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    # ---- Verificaciones ----

    def esta_en_pagina_inventario(self) -> bool:
        """True si estamos en la página de inventario."""
        return "/inventory.html" in self.driver.current_url
