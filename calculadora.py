def sumar(a, b):
    return a + b
    
def restar(a, b):
    return a - b
    
def multiplicar(a, b):
    return a * b
    
def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir por cero.") # Lanzamos la excepción
    return a / b

##

def calculadora():
    try:
        a = float(input("Primer número: "))
        b = float(input("Segundo número: "))
        print("1) Sumar | 2) Restar | 3) Multiplicar | 4) Dividir")
        opcion = input("Elije (1-4): ")
        
        if opcion == '1': resultado = sumar(a, b)
        elif opcion == '2': resultado = restar(a, b)
        elif opcion == '3': resultado = multiplicar(a, b)
        elif opcion == '4': resultado = dividir(a, b)
        else: 
            print("Opción inválida.")
            return # Cortamos la ejecución
            
        print(f"Resultado: {resultado}")
        
    except ValueError as e: # Atrapa tanto el error de dividir por 0 como el de ingresar letras
        print(f"Error: {e}")
    except Exception as e: # Por si hay cualquier otro error no contemplado
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == '__main__':
    calculadora()