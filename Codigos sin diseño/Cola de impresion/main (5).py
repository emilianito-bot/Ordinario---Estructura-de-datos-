import random  # Permite elegir un equipo al azar para simular trabajos entrantes

cola = []  # Estructura FIFO: el primer trabajo en entrar será el primero en imprimirse
capacidad_maxima = 6  # Límite máximo de trabajos permitidos en la cola
pcs = ["PC1", "PC2", "PC3", "PC4", "PC5"]  # Equipos disponibles que envían impresiones

opcion = ""

# Bucle principal del menú: se repite hasta que el usuario elija salir (opción "3")
while opcion != "3":
    print("\n--------------------------------")
    print("Estado actual de la cola:", cola)
    print("Espacio ocupado:", len(cola), "de", capacidad_maxima)
    print("--------------------------------")

    print("1. Agregar trabajo")
    print("2. Imprimir documento")
    print("3. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        # Desbordamiento (overflow): bloquea la inserción si ya alcanzó el límite
        if len(cola) >= capacidad_maxima:
            print("\n La cola de impresión está LLENA")
        else:
            pc_aleatoria = random.choice(pcs)
            cola.append(pc_aleatoria)  # Enqueue: inserta el nuevo trabajo al final
            print("\nSe agregó:", pc_aleatoria)

    elif opcion == "2":
        # Subdesbordamiento (underflow): evita intentar atender si no hay elementos
        if len(cola) == 0:
            print("\n La cola de impresión está VACÍA")
        else:
            atendido = cola.pop(0)  # Dequeue: extrae y atiende el elemento del frente (índice 0)
            print("\nImpresión:", atendido)

    elif opcion == "3":
        print("\n¡Hasta luego!")

    else:
        print("\nOpción no válida, intenta de nuevo.")