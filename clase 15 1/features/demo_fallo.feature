# ⚠️ DEMO: este escenario FALLA A PROPÓSITO para verificar el hook de
# capturas automáticas (after_step). No tiene tags @smoke ni @regression,
# así que NO corre dentro de Pytest; solo aparece al correr  behave  completo.
@demo
Característica: Demostración de captura en fallos
  Como tester
  Quiero evidenciar que un paso fallido genera una captura automática
  Para cumplir el checklist de QA-158

  Antecedentes:
    Dado que estoy en la página de login

  Escenario: Fallo a propósito para generar captura
    Cuando ingreso usuario "standard_user" y clave "secret_sauce"
    Entonces la URL contiene "checkout-complete.html"
