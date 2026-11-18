# Ticket QA-158 — Tarea 1: Escenarios de autenticación en Gherkin
@ui
Característica: Login en SauceDemo
  Como usuario registrado
  Quiero poder autenticarme con mis credenciales
  Para acceder al inventario de productos

  Antecedentes:
    Dado que estoy en la página de login

  @smoke
  Escenario: Login exitoso con credenciales válidas
    Cuando ingreso usuario "standard_user" y clave "secret_sauce"
    Entonces la URL contiene "inventory.html"
    Y veo el título "Products"

  Esquema del escenario: Casos de error de login
    Cuando ingreso usuario "<usuario>" y clave "<clave>"
    Entonces veo el mensaje de error "<mensaje>"

    Ejemplos:
      | usuario          | clave          | mensaje                            |
      | usuario_invalido | clave_invalida | Username and password do not match |
      | locked_out_user  | secret_sauce   | locked out                         |
      | vacío            | secret_sauce   | Username is required               |
      | standard_user    | vacío          | Password is required               |
