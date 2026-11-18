# utils/datos.py

import csv
import json
import pathlib


def leer_csv_login(ruta_archivo):
    """
    Lee un archivo CSV de credenciales de login y devuelve una lista de tuplas
    para usar en parametrizacion de pytest.

    Formato esperado del CSV:
        usuario,clave,debe_funcionar,descripcion

    Retorna:
        Lista de tuplas: (usuario, clave, debe_funcionar, descripcion)
    """
    datos = []
    ruta = pathlib.Path(ruta_archivo)

    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            # Convertir string 'True'/'False' a booleano
            debe_funcionar = fila['debe_funcionar'].strip().lower() == 'true'
            datos.append((
                fila['usuario'].strip(),
                fila['clave'].strip(),
                debe_funcionar,
                fila['descripcion'].strip()
            ))

    return datos


def leer_json_productos(ruta_archivo):
    """
    Lee un archivo JSON con informacion de productos y devuelve una lista
    de diccionarios para usar en parametrizacion de pytest.

    Formato esperado del JSON:
        [{"nombre": "...", "precio": 29.99, "descripcion": "..."}, ...]

    Retorna:
        Lista de diccionarios con los datos de cada producto.
    """
    ruta = pathlib.Path(ruta_archivo)

    with open(ruta, 'r', encoding='utf-8') as archivo:
        productos = json.load(archivo)

    return productos


def leer_json_nombres_productos(ruta_archivo):
    """
    Lee un archivo JSON de productos y devuelve solo los nombres.
    Util para parametrizacion simple por nombre de producto.

    Retorna:
        Lista de strings con los nombres de productos.
    """
    productos = leer_json_productos(ruta_archivo)
    return [producto['nombre'] for producto in productos]


# === Ejemplo de uso (para probar las funciones independientemente) ===
if __name__ == "__main__":
    # Probar lectura de CSV
    casos_login = leer_csv_login('datos/login.csv')
    print("=== Datos de Login (CSV) ===")
    for caso in casos_login:
        print(f"  {caso}")

    # Probar lectura de JSON
    productos = leer_json_productos('datos/productos.json')
    print("\n=== Datos de Productos (JSON) ===")
    for prod in productos:
        print(f"  {prod['nombre']} - ${prod['precio']}")

    # Probar solo nombres
    nombres = leer_json_nombres_productos('datos/productos.json')
    print(f"\n=== Nombres de Productos ===")
    print(f"  {nombres}")
