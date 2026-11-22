import os  # Permite interactuar con el sistema operativo (en este caso, limpiar la consola).

class NavegadorWeb:
    def __init__(self, capacidad_maxima=5):
        """
        EXPOSICIÓN - Constructor (__init__):
        Inicializa el estado del navegador. Usamos dos listas como pilas (LIFO):
        - back_stack guarda el historial para retroceder.
        - forward_stack guarda las páginas a las que avanzamos tras retroceder.
        - capacidad_maxima limita cuántas páginas se conservan en 'atrás'.
        """
        self.pagina_actual = "Ninguna (Inicio)"
        self.back_stack = []
        self.forward_stack = []
        self.capacidad_maxima = capacidad_maxima
        self.mensaje_notificacion = ""

    def mostrar_pila(self, pila):
        """
        EXPOSICIÓN - Visualización de una pila:
        Recorre la pila en reversa para mostrar el 'tope' (último elemento en entrar)
        arriba, reflejando visualmente el comportamiento LIFO.
        """
        if not pila:
            print("  (Vacío)")
            return
        # Muestra desde el elemento superior (tope) hacia abajo
        for i, elem in enumerate(reversed(pila), 1):
            print(f"  [{len(pila) - i + 1}] {elem}")

    def visitar(self, url):
        """
        EXPOSICIÓN - Visitar nueva URL:
        1. Si ya había una página activa, la envía a la pila 'atrás' (append).
        2. Si 'atrás' está llena, elimina la más antigua (pop(0)) para respetar el límite.
        3. Actualiza la página actual y vacía 'adelante', porque al abrir una ruta nueva
           se pierde el historial futuro de esa rama.
        """
        if self.pagina_actual and self.pagina_actual != "Ninguna (Inicio)":
            # Si la pila atrás alcanzó su límite, removemos el elemento más antiguo (el fondo)
            if len(self.back_stack) >= self.capacidad_maxima:
                self.back_stack.pop(0)

            self.back_stack.append(self.pagina_actual)
            self.mensaje_notificacion = f"[!] Visitando nueva página: {url}"
        else:
            self.mensaje_notificacion = f"[!] Visitando nueva página: {url}"

        self.pagina_actual = url
        # Al visitar una nueva página, la pila adelante se limpia por completo
        self.forward_stack.clear()

    def back(self):
        """
        EXPOSICIÓN - Operación Retroceder (Back):
        Valida que haya historial previo. Guarda la página actual en 'forward_stack'
        (por si luego queremos avanzar) y extrae el tope de 'back_stack' (pop) como
        la nueva página actual.
        """
        if not self.back_stack:
            self.mensaje_notificacion = (
                "[ERROR 404] PILA VACÍA: No hay páginas en la pila atrás para retroceder."
            )
            return

        self.forward_stack.append(self.pagina_actual)
        self.pagina_actual = self.back_stack.pop()
        self.mensaje_notificacion = f"[<-] Retrocediendo a: {self.pagina_actual}"

    def forward(self):
        """
        EXPOSICIÓN - Operación Avanzar (Forward):
        Solo funciona si antes se retrocedió. Mueve la página actual a 'back_stack'
        (respetando la capacidad máxima) y saca el tope de 'forward_stack' (pop).
        """
        if not self.forward_stack:
            self.mensaje_notificacion = (
                "[ERROR 404] PILA VACÍA: No hay páginas en la pila adelante para avanzar."
            )
            return

        # Gestionar la capacidad máxima antes de guardar la página actual en la pila atrás
        if len(self.back_stack) >= self.capacidad_maxima:
            self.back_stack.pop(0)

        self.back_stack.append(self.pagina_actual)

        # Extraer la siguiente página de la pila adelante
        self.pagina_actual = self.forward_stack.pop()
        self.mensaje_notificacion = f"[->] Avanzando a: {self.pagina_actual}"

    def mostrar_estado(self):
        """
        EXPOSICIÓN - Interfaz de estado en consola:
        Dibuja en pantalla ambas pilas, su ocupación respecto al máximo y la página
        activa, junto con el último mensaje o alerta para que el usuario vea el cambio.
        """
        print("=" * 54)
        print("                 ESTADO DEL NAVEGADOR                  ")
        print("=" * 54)
        # 1. Muestra la pila adelante primero
        print(" PILA ADELANTE (Forward Stack):")
        self.mostrar_pila(self.forward_stack)
        print("-" * 54)
        # 2. Muestra la pila atrás después
        print(f" PILA ATRÁS (Back Stack) [{len(self.back_stack)}/{self.capacidad_maxima}]:")
        self.mostrar_pila(self.back_stack)
        print("-" * 54)
        # 3. Muestra la página actual al final
        print(f" PÁGINA ACTUAL: {self.pagina_actual}")
        print("=" * 54)

        # Muestra notificaciones o errores del último movimiento
        if self.mensaje_notificacion:
            print(f"\n{self.mensaje_notificacion}\n" + "-" * 54)


def limpiar_pantalla():
    """
    EXPOSICIÓN - Limpieza de terminal:
    Detecta si el sistema es Windows ('nt') o Unix/Linux/macOS para ejecutar
    el comando correspondiente y mantener la vista limpia en cada turno.
    """
    # Ejecuta 'cls' en Windows o 'clear' en Linux/macOS
    os.system("cls" if os.name == "nt" else "clear")


def main():
    """
    EXPOSICIÓN - Bucle principal (Control de flujo):
    Crea una instancia del navegador y mantiene un ciclo infinito hasta que el
    usuario elige salir, leyendo la opción y delegando a los métodos de la clase.
    """
    navegador = NavegadorWeb(capacidad_maxima=5)

    while True:
        limpiar_pantalla()
        navegador.mostrar_estado()

        print("\n Menú :")
        print("1. Visitar página (URL)")
        print("2. Retroceder (Back)")
        print("3. Avanzar (Forward)")
        print("4. Salir (Exit)")

        opcion = input("\nSelecciona una opción (1-4): ").strip()

        if opcion == "1":
            url = input("Ingresa la URL: ").strip()
            if url:
                navegador.visitar(url)
            else:
                navegador.mensaje_notificacion = "[ERROR] La URL no puede estar vacía."
        elif opcion == "2":
            navegador.back()
        elif opcion == "3":
            navegador.forward()
        elif opcion == "4":
            limpiar_pantalla()
            print("Cerrando el navegador...")
            break
        else:
            navegador.mensaje_notificacion = "[ERROR] Opción no válida. Intenta de nuevo."


# EXPOSICIÓN - Punto de entrada: asegura que main() solo corra si el archivo se ejecuta directamente.
if __name__ == "__main__":
    main()