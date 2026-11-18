"""
pages/login_page.py — Page Object de la página de login de SauceDemo.

Encapsula selectores y acciones: los tests (Pytest o BDD) solo cuentan la
intención del usuario, nunca los selectores CSS.

Nota técnica: incluye esperas explícitas y un fallback por JS porque en
headless el navegador puede perder el foco (document.hasFocus() = False)
y los eventos de teclado/ratón del driver no llegan a la página (la app
es React y controla los inputs). El fallback setea el valor por JS
disparando los eventos input/change que React espera, y repite el clic
por JS esperando la reacción de la app (URL o mensaje de error).
"""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL_LOGIN = "https://www.saucedemo.com"
ESPERA_MAX = 10  # segundos (esperas explícitas)

# Setea el valor de un input por JS y dispara los eventos que React espera
_SET_VALOR_JS = """
const [el, txt] = arguments;
const setter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value').set;
setter.call(el, txt);
el.dispatchEvent(new Event('input',  { bubbles: true }));
el.dispatchEvent(new Event('change', { bubbles: true }));
"""


class LoginPage:
    """Page Object para la página de login de SauceDemo."""

    # 📍 Locators: el ÚNICO lugar a editar si cambian los atributos HTML
    _USUARIO = (By.ID, "user-name")
    _CLAVE = (By.ID, "password")
    _BOTON_LOGIN = (By.ID, "login-button")
    _MENSAJE_ERROR = (By.CSS_SELECTOR, 'h3[data-test="error"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ESPERA_MAX)

    # ---- Acciones de alto nivel (method chaining) ----

    def abrir(self):
        """Abre la página de login y espera a que el formulario esté listo."""
        self.driver.get(URL_LOGIN)
        self.wait.until(EC.element_to_be_clickable(self._BOTON_LOGIN))
        return self

    def _escribir(self, locator, texto: str):
        """Escribe texto en un input de forma robusta:
        1) send_keys normal; 2) si el valor no 'pegó' (página sin foco),
        lo setea por JS con los eventos de React."""
        elemento = self.driver.find_element(*locator)
        elemento.clear()
        if texto:
            elemento.send_keys(texto)
            if elemento.get_attribute("value") != texto:
                self.driver.execute_script(_SET_VALOR_JS, elemento, texto)
        return elemento

    def completar_usuario(self, usuario: str):
        """Escribe el nombre de usuario (alias legible)."""
        self._escribir(self._USUARIO, usuario or "")
        return self

    def completar_clave(self, clave: str):
        """Escribe la contraseña (alias legible)."""
        self._escribir(self._CLAVE, clave or "")
        return self

    def ingresar_credenciales(self, usuario: str, clave: str):
        """Escribe usuario y clave en el formulario ('' o None = dejar vacío)."""
        self._escribir(self._USUARIO, usuario or "")
        self._escribir(self._CLAVE, clave or "")
        return self

    def hacer_clic_login(self):
        """Presiona el botón de login y ESPERA la reacción de la app:
        redirección al inventario (éxito) o mensaje de error (fallo).
        Si el clic nativo no tuvo efecto, lo repite por JS."""
        reaccion = EC.any_of(
            EC.url_contains("inventory.html"),
            EC.visibility_of_element_located(self._MENSAJE_ERROR),
        )
        try:
            WebDriverWait(self.driver, 3).until(reaccion)
        except TimeoutException:
            boton = self.driver.find_element(*self._BOTON_LOGIN)
            self.driver.execute_script("arguments[0].click();", boton)
            WebDriverWait(self.driver, ESPERA_MAX).until(reaccion)
        return self

    def hacer_click_login(self):
        """Alias en español del clic (compatibilidad con steps)."""
        return self.hacer_clic_login()

    def login_completo(self, usuario: str, clave: str):
        """Flujo completo: abrir → credenciales → login."""
        return (
            self.abrir()
            .ingresar_credenciales(usuario, clave)
            .hacer_clic_login()
        )

    # ---- Helpers de consulta (sin asserts dentro de la página) ----

    def texto_error(self) -> str:
        """Devuelve el texto del mensaje de error visible."""
        self.wait.until(EC.visibility_of_element_located(self._MENSAJE_ERROR))
        return self.driver.find_element(*self._MENSAJE_ERROR).text

    def obtener_mensaje_error(self) -> str:
        """Alias legible: devuelve el texto del error (o '' si no hay)."""
        try:
            return self.texto_error()
        except Exception:
            return ""

    def esta_error_visible(self) -> bool:
        """True si hay un mensaje de error visible en la página."""
        try:
            self.wait.until(EC.visibility_of_element_located(self._MENSAJE_ERROR))
            return True
        except Exception:
            return False

    def esta_en_pagina_login(self) -> bool:
        """True si seguimos en la página de login (no redirigió)."""
        return "saucedemo.com" in self.driver.current_url
