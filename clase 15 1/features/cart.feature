# Ticket QA-158 — Tarea 2: Funcionalidad de carrito en Gherkin
@ui @regression
Característica: Carrito de compras en SauceDemo
  Como comprador
  Quiero agregar productos al carrito
  Para revisar mi compra antes de pagarla

  Antecedentes:
    Dado que inicié sesión como "standard_user"
    Y estoy en la página de inventario

  Escenario: Agregar un producto al carrito
    Cuando agrego el producto "Sauce Labs Backpack"
    Entonces el contador del carrito muestra "1"

  Escenario: Agregar múltiples productos al carrito
    Cuando agrego el producto "Sauce Labs Backpack"
    Y agrego el producto "Sauce Labs Bike Light"
    Entonces el contador del carrito muestra "2"
