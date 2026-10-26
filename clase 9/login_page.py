# pages/login_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object para la pagina de login de SauceDemo."""

    # 1. IDENTIDAD DE LA PAGINA
    URL = "https://www.saucedemo.com/"

    # 2. LOCATORS (privados y centralizados)
    _USER_INPUT = (By.ID, "user-name")
    _PASS_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        """
        3. INYECCION DE DEPENDENCIAS
        Recibe la instancia de WebDriver desde el fixture en conftest.py.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # 4. METODOS DE NAVEGACION Y ACCION
    def abrir(self):
        """Carga la URL de login en el navegador."""
        self.driver.get(self.URL)
        return self

    def completar_usuario(self, usuario: str):
        """Escribe el nombre de usuario."""
        campo = self.wait.until(EC.visibility_of_element_located(self._USER_INPUT))
        campo.clear()
        campo.send_keys(usuario)
        return self

    def completar_clave(self, clave: str):
        """Escribe la contrasena."""
        campo = self.driver.find_element(*self._PASS_INPUT)
        campo.clear()
        campo.send_keys(clave)
        return self

    def hacer_clic_login(self):
        """Hace clic en el boton Login."""
        self.driver.find_element(*self._LOGIN_BUTTON).click()
        return self

    def login_completo(self, usuario, clave):
        """Metodo de conveniencia para hacer login completo en un solo paso."""
        self.completar_usuario(usuario)
        self.completar_clave(clave)
        self.hacer_clic_login()
        return self

    # 5. METODOS DE VERIFICACION (retornan datos, NO hacen asserts)
    def esta_error_visible(self) -> bool:
        """Comprueba si aparece un mensaje de error en la pagina."""
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE))
            return True
        except:
            return False

    def obtener_mensaje_error(self) -> str:
        """Obtiene el texto del mensaje de error."""
        if self.esta_error_visible():
            return self.driver.find_element(*self._ERROR_MESSAGE).text
        return ""

    def esta_en_pagina_login(self) -> bool:
        """Verifica si estamos en la pagina de login."""
        return "saucedemo.com" in self.driver.current_url
