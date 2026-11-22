import random
import numpy as np

class Resistencia:
    def __init__(self):
        # Arreglo de colores según la tabla estándar
        self.colores = np.array([
            "Negro",    # 0
            "Marrón",   # 1
            "Rojo",     # 2
            "Naranja",  # 3
            "Amarillo", # 4
            "Verde",    # 5
            "Azul",     # 6
            "Violeta",  # 7
            "Gris",     # 8
            "Blanco"    # 9
        ])

    def determinar_colores(self, valor):
        str_val = str(int(valor))
        # Tomamos los dos primeros dígitos significativos
        banda1 = self.colores[int(str_val[0])]
        banda2 = self.colores[int(str_val[1])]
        
        # El multiplicador corresponde a la cantidad de ceros restantes (longitud - 2)
        mult_index = len(str_val) - 2
        banda3 = self.colores[mult_index]
        
        return np.array([banda1, banda2, banda3])

    def calcular_serie(self, n):
        resistencias = np.array([random.randint(10, 1000000000) for _ in range(n)])
        rts = np.sum(resistencias) # Usando funciones vectorizadas de NumPy
        return resistencias, rts

    def calcular_paralelo(self, n):
        resistencias = np.array([random.randint(10, 1000000000) for _ in range(n)])
        # Suma de los inversos
        suma_inversos = np.sum(1.0 / resistencias)
        # Aplicamos el inverso para obtener la resistencia equivalente total en ohmios
        rtp = 1.0 / suma_inversos
        return resistencias, rtp


if __name__ == "__main__":
    resistencia = Resistencia()

    while True:
        print("\n--- MENÚ RESISTENCIAS ---")
        print("1. Determinar colores")
        print("2. Resistencias en serie")
        print("3. Resistencias en paralelo")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            try:
                valor = int(input("Ingresa el valor de la resistencia (ej. 160, 5800): "))
                bandas = resistencia.determinar_colores(valor)
                print(f"Salida: {bandas[0]}, {bandas[1]}, {bandas[2]}")
            except (ValueError, IndexError):
                print("Error: Ingrese un valor entero válido y mayor o igual a 10.")

        elif opcion == "2":
            n = int(input("¿Cuántas resistencias?: "))
            resistencias, rts = resistencia.calcular_serie(n)
            print("Resistencias:", resistencias)
            print(f"Rts = {rts:,.2f} Ω")

        elif opcion == "3":
            n = int(input("¿Cuántas resistencias?: "))
            resistencias, rtp = resistencia.calcular_paralelo(n)
            print("Resistencias:", resistencias)
            print(f"Rtp = {rtp:,.2f} Ω")

        elif opcion == "4":
            print("Fin del programa")
            break
        else:
            print("Opción inválida, intenta de nuevo.")