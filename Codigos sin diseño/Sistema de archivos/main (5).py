# Sistema de archivos simulado mediante un Árbol Binario de Búsqueda (ABB)
from abc import ABC       # Permite crear clases abstractas (clases base que no se instancian solas)
from enum import Enum     # Permite definir conjuntos de constantes con nombre (TipoNodo)


class TipoNodo(Enum):
    """Define los dos tipos válidos de elementos dentro del sistema de archivos."""
    DIRECTORIO = "Directorio"
    ARCHIVO = "Archivo"


class Nodo(ABC):
    """Clase base abstracta que representa un elemento genérico (archivo o directorio) en el árbol."""

    def __init__(self, nombre: str, extension: str, tamano: int, tipo: TipoNodo):
        # Atributos principales del elemento
        self.nombre = nombre
        self.extension = extension
        self.tamano = tamano
        self.tipo = tipo
        # Apuntadores a los hijos en el Árbol Binario de Búsqueda (izquierdo y derecho)
        self.izq = None
        self.der = None

    def mostrar_informacion(self):
        """Imprime en consola los datos detallados del nodo."""
        # Si no tiene extensión (como un directorio), muestra '(ninguna)'
        ext = self.extension if self.extension else "(ninguna)"
        print("-" * 35)
        print(f"Nombre:    {self.nombre}")
        print(f"Tipo:      {self.tipo.value}")
        print(f"Extensión: {ext}")
        print(f"Tamaño:    {self.tamano} bytes")
        print("-" * 35)


class Directorio(Nodo):
    """Subclase de Nodo para directorios: siempre sin extensión y con tamaño inicial 0."""

    def __init__(self, nombre: str):
        super().__init__(nombre, "", 0, TipoNodo.DIRECTORIO)


class Archivo(Nodo):
    """Subclase de Nodo para archivos: requiere nombre, extensión y tamaño en bytes."""

    def __init__(self, nombre: str, extension: str, tamano: int):
        super().__init__(nombre, extension, tamano, TipoNodo.ARCHIVO)


class ArbolBinarioBusqueda:
    """Estructura de datos ABB que organiza los nodos alfabéticamente por nombre (sin distinguir mayúsculas)."""

    def __init__(self):
        # Inicializa el árbol con un directorio raíz fijo llamado "Documentos"
        self.raiz = Directorio("Documentos")

    def insertar(self, nuevo_nodo: Nodo) -> bool:
        """Valida e inserta un nuevo nodo en el ABB. Retorna True si tuvo éxito, False si falló."""
        if nuevo_nodo is None:
            return False

        # Evita duplicar el nombre del directorio raíz
        if nuevo_nodo.nombre.lower() == self.raiz.nombre.lower():
            print("ERROR: El elemento ya existe (es el directorio raíz).")
            return False

        # Llama al método recursivo de inserción comenzando desde la raíz
        return self._insertar_rec(self.raiz, nuevo_nodo)

    def _insertar_rec(self, actual: Nodo, nuevo_nodo: Nodo) -> bool:
        """Recorre recursivamente el árbol para ubicar 'nuevo_nodo' según el orden alfabético."""
        # Comparación insensible a mayúsculas/minúsculas para evitar nombres repetidos
        if nuevo_nodo.nombre.lower() == actual.nombre.lower():
            print(f"ERROR: El elemento '{nuevo_nodo.nombre}' ya existe en el sistema.")
            return False

        # Si el nombre es menor alfabéticamente, va hacia el subárbol izquierdo
        if nuevo_nodo.nombre.lower() < actual.nombre.lower():
            # Regla del simulador: un nodo tipo ARCHIVO no puede tener hijos debajo de él
            if actual.tipo == TipoNodo.ARCHIVO:
                print("ERROR: No se puede insertar el elemento.")
                print("Un archivo no puede contener otros elementos.")
                return False
            # Si el espacio izquierdo está libre, inserta ahí; si no, sigue bajando
            if actual.izq is None:
                actual.izq = nuevo_nodo
                return True
            return self._insertar_rec(actual.izq, nuevo_nodo)

        # Si el nombre es mayor alfabéticamente, va hacia el subárbol derecho
        else:
            if actual.tipo == TipoNodo.ARCHIVO:
                print("ERROR: No se puede insertar el elemento.")
                print("Un archivo no puede contener otros elementos.")
                return False
            if actual.der is None:
                actual.der = nuevo_nodo
                return True
            return self._insertar_rec(actual.der, nuevo_nodo)

    def buscar(self, nombre: str):
        """Busca un nodo por su nombre dentro del ABB y devuelve el objeto Nodo o None si no existe."""
        return self._buscar_rec(self.raiz, nombre)

    def _buscar_rec(self, actual, nombre: str):
        """Búsqueda binaria recursiva: descarta la mitad del árbol en cada paso."""
        if actual is None:
            return None
        if nombre.lower() == actual.nombre.lower():
            return actual
        if nombre.lower() < actual.nombre.lower():
            return self._buscar_rec(actual.izq, nombre)
        return self._buscar_rec(actual.der, nombre)

    def eliminar(self, nombre: str) -> bool:
        """Valida reglas de eliminación y borra un nodo del árbol si es válido."""
        # Protege el directorio raíz para que no pueda eliminarse
        if nombre.lower() == self.raiz.nombre.lower():
            print("ERROR: No se puede eliminar el directorio raíz principal.")
            return False

        # Verifica que el nodo exista antes de intentar borrarlo
        objetivo = self.buscar(nombre)
        if objetivo is None:
            print("El elemento no existe en el sistema de archivos.")
            return False

        # Evita borrar un directorio si tiene hijos (izq o der) en el árbol
        if objetivo.tipo == TipoNodo.DIRECTORIO and (
            objetivo.izq is not None or objetivo.der is not None
        ):
            print(
                f"ERROR: No se puede eliminar el directorio '{nombre}' "
                "porque contiene elementos en el sistema."
            )
            return False

        # Actualiza la raíz (por si cambió en la recursión) y elimina el nodo
        self.raiz = self._eliminar_rec(self.raiz, nombre)
        return True

    def _eliminar_rec(self, actual, nombre: str):
        """Elimina un nodo del ABB considerando los 3 casos clásicos (0, 1 o 2 hijos)."""
        if actual is None:
            return None

        # Avanza hacia la izquierda o derecha buscando el nodo a eliminar
        if nombre.lower() < actual.nombre.lower():
            actual.izq = self._eliminar_rec(actual.izq, nombre)
        elif nombre.lower() > actual.nombre.lower():
            actual.der = self._eliminar_rec(actual.der, nombre)
        else:
            # Nodo encontrado:
            # Caso 1: Sin hijos (hoja) -> se elimina devolviendo None
            if actual.izq is None and actual.der is None:
                return None
            # Caso 2a: Solo tiene hijo derecho -> sube el hijo derecho
            if actual.izq is None:
                return actual.der
            # Caso 2b: Solo tiene hijo izquierdo -> sube el hijo izquierdo
            if actual.der is None:
                return actual.izq

            # Caso 3: Tiene dos hijos -> se reemplaza con el sucesor inorden (menor del subárbol derecho)
            sucesor = self._obtener_minimo(actual.der)
            actual.nombre = sucesor.nombre
            actual.extension = sucesor.extension
            actual.tamano = sucesor.tamano
            actual.tipo = sucesor.tipo
            # Elimina el nodo sucesor duplicado del subárbol derecho
            actual.der = self._eliminar_rec(actual.der, sucesor.nombre)

        return actual

    def _obtener_minimo(self, nodo: Nodo) -> Nodo:
        """Encuentra el nodo con menor valor (más a la izquierda) a partir de 'nodo'."""
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual

    # --- Recorridos del árbol ---
    # Inorden: Izquierda -> Raíz -> Derecha (muestra los elementos ordenados alfabéticamente)
    def recorrer_inorden(self, nodo):
        if nodo is not None:
            self.recorrer_inorden(nodo.izq)
            nodo.mostrar_informacion()
            self.recorrer_inorden(nodo.der)

    # Preorden: Raíz -> Izquierda -> Derecha (útil para copiar o ver la estructura desde la raíz)
    def recorrer_preorden(self, nodo):
        if nodo is not None:
            nodo.mostrar_informacion()
            self.recorrer_preorden(nodo.izq)
            self.recorrer_preorden(nodo.der)

    # Postorden: Izquierda -> Derecha -> Raíz (útil para liberar/eliminar nodos de abajo hacia arriba)
    def recorrer_postorden(self, nodo):
        if nodo is not None:
            self.recorrer_postorden(nodo.izq)
            self.recorrer_postorden(nodo.der)
            nodo.mostrar_informacion()


def main():
    """Función principal: gestiona el menú interactivo en consola y valida entradas del usuario."""
    arbol = ArbolBinarioBusqueda()
    opcion = 0

    while opcion != 9:
        print("\n========== SISTEMA DE ARCHIVOS (ABB) ==========")
        print("1. Crear directorio")
        print("2. Insertar archivo")
        print("3. Buscar elemento por nombre")
        print("4. Eliminar elemento")
        print("5. Mostrar recorrido Inorden")
        print("6. Mostrar recorrido Preorden")
        print("7. Mostrar recorrido Postorden")
        print("8. Mostrar información de un elemento")
        print("9. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
            continue

        if opcion == 1:
            # Opción 1: Crea un directorio validando que el nombre no esté vacío
            nom_dir = input("Nombre del directorio: ").strip()
            if not nom_dir:
                print("El nombre del elemento no puede estar vacío.")
                continue
            if arbol.insertar(Directorio(nom_dir)):
                print("Directorio creado exitosamente.")

        elif opcion == 2:
            # Opción 2: Crea un archivo validando nombre, extensión y tamaño entero >= 0
            nom_arch = input("Nombre del archivo: ").strip()
            ext_arch = input("Extensión (ej. pdf, txt, jpg): ").strip()
            if not nom_arch:
                print("El nombre del elemento no puede estar vacío.")
                continue
            if not ext_arch:
                print("ERROR: Un archivo debe tener extensión.")
                continue
            try:
                tam_arch = int(input("Tamaño en bytes (>= 0): "))
            except ValueError:
                print("ERROR: El tamaño debe ser un número entero.")
                continue
            if tam_arch < 0:
                print("ERROR: El tamaño del archivo debe ser mayor o igual a cero.")
                continue
            if arbol.insertar(Archivo(nom_arch, ext_arch, tam_arch)):
                print("Archivo insertado exitosamente.")

        elif opcion == 3:
            # Opción 3: Busca un nodo por nombre y muestra sus datos si existe
            nom_buscar = input("Nombre del elemento a buscar: ").strip()
            encontrado = arbol.buscar(nom_buscar)
            if encontrado is not None:
                print("\nElemento encontrado:")
                encontrado.mostrar_informacion()
            else:
                print("El elemento no existe en el sistema de archivos.")

        elif opcion == 4:
            # Opción 4: Intenta eliminar un elemento por nombre respetando las reglas del sistema
            nom_elim = input("Nombre del elemento a eliminar: ").strip()
            if arbol.eliminar(nom_elim):
                print("Elemento eliminado exitosamente.")

        elif opcion == 5:
            # Opción 5: Recorrido Inorden
            print("\n--- RECORRIDO INORDEN ---")
            arbol.recorrer_inorden(arbol.raiz)

        elif opcion == 6:
            # Opción 6: Recorrido Preorden
            print("\n--- RECORRIDO PREORDEN ---")
            arbol.recorrer_preorden(arbol.raiz)

        elif opcion == 7:
            # Opción 7: Recorrido Postorden
            print("\n--- RECORRIDO POSTORDEN ---")
            arbol.recorrer_postorden(arbol.raiz)

        elif opcion == 8:
            # Opción 8: Consulta y muestra la información detallada de un elemento
            nom_info = input("Nombre del elemento a consultar: ").strip()
            info = arbol.buscar(nom_info)
            if info is not None:
                info.mostrar_informacion()
            else:
                print("El elemento no existe en el sistema de archivos.")

        elif opcion == 9:
            # Opción 9: Termina el bucle y cierra el programa
            print("Saliendo del sistema...")

        else:
            print("Opción no válida.")


# Punto de entrada del programa cuando se ejecuta directamente
if __name__ == "__main__":
    main()