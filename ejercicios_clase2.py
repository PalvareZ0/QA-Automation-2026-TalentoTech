# ==========================================
# ACTIVIDAD 1: Datos del usuario
# ==========================================

# Definimos variables y solicitamos los datos por teclado usando input()
nombre = input("Por favor, ingresa tu nombre: ")
edad = input("Por favor, ingresa tu edad: ")
profesion = input("Por favor, ingresa tu profesión: ")

# Imprimimos un mensaje personalizado usando los datos almacenados en las variables
print(f"\n--- Datos del Usuario ---")
print(f"Hola, mi nombre es {nombre}, tengo {edad} años y mi profesión es {profesion}.")


# ==========================================
# ACTIVIDAD 2: Primeros 10 números pares
# ==========================================

print("\n--- Primeros 10 números pares ---")

# Usamos un contador para llevar la cuenta de cuántos números pares hemos encontrado
contador_pares = 0
# Empezamos a evaluar desde el número 0
numero_actual = 0

# Usamos un bucle while porque no sabemos exactamente en qué número terminaremos, 
# solo sabemos que necesitamos encontrar 10 números pares.
while contador_pares < 10:
    
    # Usamos un condicional para validar si el número es par
    # Un número es par si el resto de dividirlo por 2 es igual a 0 (módulo %)
    if numero_actual % 2 == 0:
        # Si se cumple la condición, mostramos el número
        print(numero_actual)
        # Incrementamos nuestro contador en 1
        contador_pares += 1
        
    # Pasamos al siguiente número para continuar con el bucle
    numero_actual += 1