import random  # Permite generar números enteros aleatorios para simular valores de resistencias
import numpy as np  # Biblioteca numérica usada aquí para arreglos y operaciones vectorizadas rápidas


class Resistencia:
    """Clase que agrupa las operaciones para calcular bandas de color y resistencias equivalentes."""

    def __init__(self):
        # Tabla estándar de código de colores (el índice de cada color coincide con su valor numérico del 0 al 9)
        self.colores = np.array([
            "Negro",    # 0 -> valor 0 / multiplicador x1 (0 ceros)
            "Marrón",   # 1 -> valor 1 / multiplicador x10 (1 cero)
            "Rojo",     # 2 -> valor 2 / multiplicador x100 (2 ceros)
            "Naranja",  # 3 -> valor 3 / multiplicador x1,000 (3 ceros)
            "Amarillo", # 4 -> valor 4 / multiplicador x10,000 (4 ceros)
            "Verde",    # 5 -> valor 5 / multiplicador x100,000 (5 ceros)
            "Azul",     # 6 -> valor 6 / multiplicador x1,000,000 (6 ceros)
            "Violeta",  # 7 -> valor 7 / multiplicador x10,000,000 (7 ceros)
            "Gris",     # 8 -> valor 8 / multiplicador x100,000,000 (8 ceros)
            "Blanco"    # 9 -> valor 9 / multiplicador x1,000,000,000 (9 ceros)
        ])

    def determinar_colores(self, valor):
        """Convierte un valor en ohmios (ej. 160 -> Marrón, Azul, Marrón) a sus 3 primeras bandas."""
        # Convertimos a entero y luego a cadena de texto para leer dígito por dígito
        str_val = str(int(valor))

        # Primera y segunda banda: corresponden a los dos primeros dígitos significativos
        banda1 = self.colores[int(str_val[0])]
        banda2 = self.colores[int(str_val[1])]

        # Tercera banda (multiplicador): equivale a cuántos dígitos van después de los dos primeros
        # Por ejemplo, en 5800 (longitud 4): 4 - 2 = 2 -> índice 2 ("Rojo", multiplicador x100)
        mult_index = len(str_val) - 2
        banda3 = self.colores[mult_index]

        # Retornamos las tres bandas como un arreglo de NumPy
        return np.array([banda1, banda2, banda3])

    def calcular_serie(self, n):
        """Genera 'n' resistencias aleatorias y calcula la resistencia total en serie (Rts = R1 + R2 + ... + Rn)."""
        # Generamos 'n' valores aleatorios entre 10 Ω y 1,000,000,000 Ω (1 GΩ) y los guardamos en un arreglo
        resistencias = np.array([random.randint(10, 1000000000) for _ in range(n)])

        # En serie, la resistencia total es la suma directa de todas las resistencias
        rts = np.sum(resistencias)

        return resistencias, rts

    def calcular_paralelo(self, n):
        """Genera 'n' resistencias aleatorias y calcula la resistencia total en paralelo (1/Rt = 1/R1 + 1/R2 + ...)."""
        # Generamos 'n' resistencias aleatorias en el mismo rango (10 Ω a 1 GΩ)
        resistencias = np.array([random.randint(10, 1000000000) for _ in range(n)])

        # Calculamos la suma de los inversos (1.0 fuerza división decimal/flotante en NumPy)
        suma_inversos = np.sum(1.0 / resistencias)

        # Invertimos el resultado para obtener la resistencia equivalente total en ohmios
        rtp = 1.0 / suma_inversos

        return resistencias, rtp


# Bloque principal: solo se ejecuta si este archivo se corre directamente (no al importarlo como módulo)
if __name__ == "__main__":
    # Instanciamos (creamos) un objeto de la clase Resistencia para usar sus métodos
    resistencia = Resistencia()

    # Bucle infinito para mantener activo el menú hasta que el usuario elija salir
    while True:
        print("\n--- MENÚ RESISTENCIAS ---")
        print("1. Determinar colores")
        print("2. Resistencias en serie")
        print("3. Resistencias en paralelo")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            try:
                # Solicitamos el valor en ohmios y llamamos al método correspondiente
                valor = int(input("Ingresa el valor de la resistencia (ej. 160, 5800): "))
                bandas = resistencia.determinar_colores(valor)
                print(f"Salida: {bandas[0]}, {bandas[1]}, {bandas[2]}")
            except (ValueError, IndexError):
                # ValueError: si ingresan letras/decimales inválidos; IndexError: si el número es < 10 o muy grande
                print("Error: Ingrese un valor entero válido y mayor o igual a 10.")

        elif opcion == "2":
            # Pedimos cuántas resistencias aleatorias se van a generar y sumar en serie
            n = int(input("¿Cuántas resistencias?: "))
            resistencias, rts = resistencia.calcular_serie(n)
            print("Resistencias:", resistencias)
            # Formateamos con comas para miles y dos decimales, seguido del símbolo de ohmios (Ω)
            print(f"Rts = {rts:,.2f} Ω")

        elif opcion == "3":
            # Pedimos cuántas resistencias aleatorias se van a generar para calcular el paralelo
            n = int(input("¿Cuántas resistencias?: "))
            resistencias, rtp = resistencia.calcular_paralelo(n)
            print("Resistencias:", resistencias)
            print(f"Rtp = {rtp:,.2f} Ω")

        elif opcion == "4":
            # Rompe el ciclo while y termina el programa
            print("Fin del programa")
            break

        else:
            # Cualquier entrada distinta de 1, 2, 3 o 4
            print("Opción inválida, intenta de nuevo.")