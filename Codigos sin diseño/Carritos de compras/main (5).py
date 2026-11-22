# ==============================================================================
# Fase 4. Codificación - Sistema de Carrito de Compras
# Estructuras de Datos y Algoritmos - Universidad Anáhuac
# ==============================================================================

import os

# ==============================================================================
# CLASES DEL SISTEMA
# ==============================================================================

class Producto:
    """
    Representa un producto individual dentro del catálogo de la tienda.
    Almacena información básica como su identificador, nombre, categoría y precio.
    """
    def __init__(self, id: int, nombre: str, categoria: str, precio: float):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = float(precio)

    # --- Métodos Getters (para consultar los atributos de forma segura) ---
    def getID(self):
        return self.id

    def getNombre(self):
        return self.nombre

    def getCategoria(self):
        return self.categoria

    def getPrecio(self):
        return self.precio

    def __str__(self):
        # Define cómo se muestra el producto en forma de texto legible
        return f"{self.id} | {self.nombre} | {self.categoria} | ${self.precio:.2f}"


class ElementoCarrito:
    """
    Representa un renglón o ítem dentro del carrito de compras.
    Relaciona un objeto 'Producto' con la cantidad específica que el usuario desea comprar.
    """
    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = int(cantidad)

    def getProducto(self):
        return self.producto

    def getCantidad(self):
        return self.cantidad

    def setCantidad(self, nuevaCantidad: int):
        # Permite actualizar la cantidad de este ítem
        self.cantidad = nuevaCantidad

    def calcularSubtotal(self):
        # Multiplica el precio unitario del producto por la cantidad seleccionada
        return self.producto.getPrecio() * self.cantidad
     
    def __str__(self):
        return f"{self.producto.getID()} | {self.producto.getNombre()} | ${self.producto.getPrecio():.2f} | {self.cantidad} | ${self.calcularSubtotal():.2f}"


class CarritoDeCompras:
    """
    Clase principal que administra la lógica de la tienda: 
    el catálogo disponible y las operaciones del carrito (agregar, modificar, eliminar, etc.).
    """
    def __init__(self):
        # Listas en memoria para almacenar los productos y los elementos del carrito
        self.catalogo = []
        self.itemsCarrito = []
        self.cargarCatalogoInicial()

    def cargarCatalogoInicial(self):
        """Llena la lista del catálogo con productos predefinidos al iniciar la aplicación."""
        self.catalogo.append(Producto(1, "Teclado", "Accesorios", 450.0))
        self.catalogo.append(Producto(2, "Mouse", "Accesorios", 250.0))
        self.catalogo.append(Producto(3, "Monitor", "Electrónica", 3200.0))
        self.catalogo.append(Producto(4, "Audifonos", "Audio", 800.0))
        self.catalogo.append(Producto(5, "Memoria USB", "Almacenamiento", 180.0))

    def mostrarCatalogo(self):
        """Muestra en pantalla una tabla ordenada con todos los productos disponibles."""
        print("\n--- CATÁLOGO DE PRODUCTOS ---")
        print("ID | Producto | Categoría | Precio")
        print("-" * 40)
        for prod in self.catalogo:
            print(prod)
        print("-" * 40)

    def buscarProducto(self, criterio: str):
        """
        Busca un producto dentro del catálogo ya sea por su ID numérico o por su nombre.
        Utiliza una búsqueda secuencial (recorre la lista elemento por elemento).
        """
        criterioBusqueda = str(criterio).lower()
        for prod in self.catalogo:
            if str(prod.getID()) == criterioBusqueda or prod.getNombre().lower() == criterioBusqueda:
                return prod
        return None # Retorna None si no lo encuentra

    def agregarProducto(self, idONombre: str, cantidad: int):
        """
        Agrega un producto al carrito. Si el producto ya se encontraba en el carrito,
        únicamente incrementa su cantidad acumulada.
        """
        if cantidad <= 0:
            print("ERROR. La cantidad debe ser mayor a 0.")
            return False

        producto = self.buscarProducto(idONombre)
        if not producto:
            print("ERROR. Producto no encontrado en el catálogo.")
            return False

        # Verificamos si el producto ya existe en el carrito para solo sumar cantidad
        for item in self.itemsCarrito:
            if item.getProducto().getID() == producto.getID():
                item.setCantidad(item.getCantidad() + cantidad)
                print(f"\n¡Producto actualizado! {producto.getNombre()} | Cantidad total: {item.getCantidad()}")
                return True
        
        # Si es un producto nuevo en el carrito, creamos el elemento y lo agregamos a la lista
        nuevoItem = ElementoCarrito(producto, cantidad)
        self.itemsCarrito.append(nuevoItem)
        print(f"\nProducto: {producto.getNombre()}")
        print(f"Precio unitario: ${producto.getPrecio():.2f}")
        print("¡Producto agregado al carrito!")
        return True

    def verCarrito(self):
        """Muestra el contenido actual del carrito, incluyendo subtotales y el gran total a pagar."""
        print("\n--- CARRITO DE COMPRAS ---")
        if not self.itemsCarrito:
            print("(El carrito está vacío)")
            return

        print(f"{'ID':<4} | {'Producto':<15} | {'Precio':<8} | {'Cant.':<5} | {'Subtotal':<10}")
        print("-" * 55)
        
        for item in self.itemsCarrito:
            prod = item.getProducto()
            print(f"{prod.getID():<4} | {prod.getNombre():<15} | ${prod.getPrecio():<7.2f} | {item.getCantidad():<5} | ${item.calcularSubtotal():<9.2f}")
        
        print("-" * 55)
        print(f"TOTAL: ${self.calcularTotal():.2f}")

    def modificarCantidad(self, idProducto: int, nuevaCantidad: int):
        """Permite cambiar la cantidad exacta de un producto que ya se encuentra en el carrito."""
        if nuevaCantidad <= 0:
            print("ERROR. La cantidad debe ser mayor a 0.")
            return False

        for item in self.itemsCarrito:
            if item.getProducto().getID() == idProducto:
                print(f"Producto: {item.getProducto().getNombre()}")
                print(f"Cantidad actual: {item.getCantidad()}")
                item.setCantidad(nuevaCantidad)
                print("¡Cantidad actualizada!")
                return True
        
        print("ERROR. El producto no está en el carrito.")
        return False

    def eliminarProducto(self, idProducto: int):
        """Elimina un producto específico del carrito pidiendo una confirmación previa al usuario."""
        for i in range(len(self.itemsCarrito)):
            if self.itemsCarrito[i].getProducto().getID() == idProducto:
                print(f"Producto: {self.itemsCarrito[i].getProducto().getNombre()}")
                confirmacion = input("¿Está seguro que desea eliminar este producto? (s/n): ").strip().lower()
                if confirmacion == 's':
                    self.itemsCarrito.pop(i) # Remueve el elemento de la lista por su posición
                    print("¡Producto eliminado del carrito!")
                    return True
                else:
                    print("Operación cancelada.")
                    return False
        
        print("ERROR. El producto no está en el carrito.")
        return False

    def vaciarCarrito(self):
        """Limpia por completo todos los elementos almacenados en el carrito."""
        if not self.itemsCarrito:
            print("El carrito ya está vacío.")
            return

        self.verCarrito()
        confirmacion = input("\n¿Está seguro que desea vaciar el carrito? (s/n): ").strip().lower()
        if confirmacion == 's':
            self.itemsCarrito.clear() # Vacía la lista por completo
            print("¡Carrito vaciado!")
        else:
            print("Operación cancelada.")

    def calcularTotal(self):
        """Suma los subtotales de todos los elementos para obtener el costo total de la compra."""
        totalPagar = 0.0
        for item in self.itemsCarrito:
            totalPagar += item.calcularSubtotal()
        return totalPagar

    def calcularTotalArticulos(self):
        """Suma la cantidad física de unidades acumuladas en el carrito."""
        totalArticulos = 0
        for item in self.itemsCarrito:
            totalArticulos += item.getCantidad()
        return totalArticulos

    def finalizarCompra(self):
        """Muestra el resumen final de la transacción y procesa el cierre de la compra."""
        if not self.itemsCarrito:
            print("\nNo hay artículos en el carrito para comprar.")
            return

        print("\n--- RESUMEN DE COMPRA ---")
        print(f"{'ID':<4} | {'Producto':<15} | {'Cant.':<5} | {'Subtotal':<10}")
        print("-" * 45)
        for item in self.itemsCarrito:
            prod = item.getProducto()
            print(f"{prod.getID():<4} | {prod.getNombre():<15} | {item.getCantidad():<5} | ${item.calcularSubtotal():<9.2f}")
        
        print("-" * 45)
        print(f"Productos distintos: {len(self.itemsCarrito)}")
        print(f"Total de artículos: {self.calcularTotalArticulos()}")
        print(f"Total a pagar: ${self.calcularTotal():.2f}")
        print("\nGracias por su compra.")


# ==============================================================================
# FUNCIONES AUXILIARES Y CONTROL PRINCIPAL
# ==============================================================================

def limpiarPantalla():
    """Limpia la terminal o consola dependiendo del sistema operativo (Windows o Mac/Linux)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Función principal que controla el flujo del menú interactivo en la consola."""
    tienda = CarritoDeCompras()

    while True:
        limpiarPantalla()
        print("\n--- MENÚ PRINCIPAL - CARRITO DE COMPRAS ---")
        print("1. Mostrar catálogo")
        print("2. Buscar producto")
        print("3. Agregar producto al carrito")
        print("4. Ver carrito")
        print("5. Modificar cantidad")
        print("6. Eliminar producto")
        print("7. Vaciar carrito")
        print("8. Finalizar compra")
        print("9. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            limpiarPantalla()
            tienda.mostrarCatalogo()
            input("\nPresione ENTER para volver al menú...")

        elif opcion == "2":
            limpiarPantalla()
            tienda.mostrarCatalogo()
            busqueda = input("\nBuscar producto (Ingrese ID o Nombre): ").strip()
            resultado = tienda.buscarProducto(busqueda)
            if resultado:
                print("\n--- Resultado de la búsqueda ---")
                print(f"ID: {resultado.getID()}")
                print(f"Producto: {resultado.getNombre()}")
                print(f"Categoría: {resultado.getCategoria()}")
                print(f"Precio: ${resultado.getPrecio():.2f}")
            else:
                print("\nERROR. Producto no encontrado.")
            input("\nPresione ENTER para continuar...")

        elif opcion == "3":
            limpiarPantalla()
            tienda.mostrarCatalogo()
            idONombre = input("\nID o Nombre del producto a agregar: ").strip()
            try:
                cantidad = int(input("Cantidad: "))
                tienda.agregarProducto(idONombre, cantidad)
            except ValueError:
                # Captura el error si el usuario escribe texto en lugar de un número
                print("ERROR. Debe ingresar un valor numérico entero para la cantidad.")
            input("\nPresione ENTER para continuar...")

        elif opcion == "4":
            limpiarPantalla()
            tienda.verCarrito()
            input("\nPresione ENTER para volver al menú...")

        elif opcion == "5":
            limpiarPantalla()
            tienda.verCarrito()
            try:
                idProducto = int(input("\nID del producto a modificar: "))
                nuevaCantidad = int(input("Nueva cantidad: "))
                tienda.modificarCantidad(idProducto, nuevaCantidad)
            except ValueError:
                print("ERROR. Los valores ingresados deben ser numéricos enteros.")
            input("\nPresione ENTER para continuar...")

        elif opcion == "6":
            limpiarPantalla()
            tienda.verCarrito()
            try:
                idProducto = int(input("\nID del producto a eliminar: "))
                tienda.eliminarProducto(idProducto)
            except ValueError:
                print("ERROR. El ID debe ser un valor numérico entero.")
            input("\nPresione ENTER para continuar...")

        elif opcion == "7":
            limpiarPantalla()
            tienda.vaciarCarrito()
            input("\nPresione ENTER para volver al menú...")

        elif opcion == "8":
            limpiarPantalla()
            tienda.finalizarCompra()
            if tienda.itemsCarrito:
                tienda.itemsCarrito.clear() # Limpia el carrito al completar la venta con éxito
            input("\nPresione ENTER para volver al menú...")

        elif opcion == "9":
            limpiarPantalla()
            print("Gracias por usar el programa. ¡Hasta pronto!\nPrograma finalizado.")
            break # Rompe el ciclo while y termina el programa

        else:
            print("\nERROR. Opción no válida. Intente de nuevo.")
            input("Presione ENTER para continuar...")

# Punto de entrada de la aplicación en Python
if __name__ == "__main__":
    main()