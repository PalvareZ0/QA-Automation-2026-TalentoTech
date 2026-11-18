# Ejemplo 1 de la clase: BDD aplicado a lógica pura de Python
@unit
Característica: Multiplicación de enteros
  Para asegurar consistencia en el micro-servicio de cálculo
  Como desarrollador del equipo Backend
  Quiero verificar que la función multiplicar devuelve el producto correcto

  Esquema del escenario: Producto <a> x <b>
    Cuando multiplico <a> y <b>
    Entonces obtengo <resultado>

    Ejemplos:
      | a  | b | resultado |
      | 2  | 3 | 6         |
      | 5  | 0 | 0         |
      | 7  | 4 | 28        |
      | -3 | 2 | -6        |
