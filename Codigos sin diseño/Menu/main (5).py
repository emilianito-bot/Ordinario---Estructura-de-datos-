import os

def proyecto_resistencia():
    print("\n--- Proyecto: Cálculo de Resistencia (Ley de Ohm) ---")
    try:
        voltaje = float(input("Ingresa el voltaje (V): "))
        corriente = float(input("Ingresa la corriente (A): "))
        if corriente == 0:
            print("Error: La corriente no puede ser cero.")
        else:
            resistencia = voltaje / corriente
            print(f"Resultado: La resistencia es de {resistencia:.2f} Ohms.")
    except ValueError:
        print("Por favor, ingresa valores numéricos válidos.")

def proyecto_carrito():
    print("\n--- Proyecto: Carrito de Compras ---")
    carrito = []
    while True:
        producto = input("Ingresa un producto (o escribe 'salir' para terminar): ")
        if producto.lower() == 'salir':
            break
        if producto.strip():
            carrito.append(producto)
            print(f"'{producto}' agregado al carrito.")
    
    print("\nTu carrito final contiene:")
    if not carrito:
        print("El carrito está vacío.")
    else:
        for i, item in enumerate(carrito, 1):
            print(f"{i}. {item}")

def proyecto_navegador():
    print("\n--- Proyecto: Navegador Web (Simulador) ---")
    historial = []
    while True:
        url = input("Ingresa una URL a visitar (o escribe 'salir' para volver al menú): ")
        if url.lower() == 'salir':
            break
        historial.append(url)
        print(f"Navegando exitosamente a: {url}")
    
    print(f"\nHistorial de navegación de esta sesión: {historial}")

def proyecto_cola_impresion():
    print("\n--- Proyecto: Cola de Impresión ---")
    cola = ["documento1.pdf", "reporte.docx", "factura.pdf"]
    print(f"Cola actual: {cola}")
    
    while cola:
        accion = input("\n¿Deseas imprimir el siguiente documento en espera? (s/n): ").lower()
        if accion == 's':
            impreso = cola.pop(0)
            print(f"🖨️ Imprimiendo... [{impreso}] completado.")
            print(f"Documentos restantes en cola: {cola}")
        else:
            break
    print("La cola de impresión ha finalizado.")

def proyecto_sistema_archivos():
    print("\n--- Proyecto: Sistema de Archivos ---")
    directorio_actual = os.getcwd()
    print(f"Directorio de trabajo actual: {directorio_actual}")
    print("Archivos y carpetas en este directorio:")
    for elemento in os.listdir(directorio_actual):
        print(f" - {elemento}")

def proyecto_ruta_magica():
    print("\n--- Proyecto: Ruta Mágica ---")
    print("✨ ¡Bienvenido a la Ruta Mágica! ✨")
    destino = input("¿A qué dimensión o destino mágico deseas viajar?: ")
    print(f"Abriendo portales hacia: {destino}...")
    print(f"¡Has llegado con éxito a {destino}! Disfruta la magia.")

def mostrar_menu():
    while True:
        print("\n==============================")
        print("       MENÚ DE PROYECTOS      ")
        print("==============================")
        print("1. Resistencia")
        print("2. Carrito de compras")
        print("3. Navegador web")
        print("4. Cola de impresión")
        print("5. Sistema de archivos")
        print("6. Ruta mágica")
        print("7. Salir")
        print("==============================")
        
        opcion = input("Elige una opción (1-7): ")
        
        if opcion == '1':
            proyecto_resistencia()
        elif opcion == '2':
            proyecto_carrito()
        elif opcion == '3':
            proyecto_navegador()
        elif opcion == '4':
            proyecto_cola_impresion()
        elif opcion == '5':
            proyecto_sistema_archivos()
        elif opcion == '6':
            proyecto_ruta_magica()
        elif opcion == '7':
            print("\n¡Gracias por usar el menú de proyectos! Hasta luego.")
            break
        else:
            print("\nOpción no válida. Por favor, elige un número entre 1 y 7.")

if __name__ == "__main__":
    mostrar_menu()