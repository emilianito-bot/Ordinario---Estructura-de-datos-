import random
import tkinter as tk
from tkinter import messagebox

class ResistenciaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto: Calculadora y Gráfico de Resistencias")
        self.root.geometry("550x520")
        self.root.config(bg="#f4f4f9")

        # Diccionario con los colores y sus códigos de diseño gráfico en HEX
        self.colores_dict = {
            "Negro": {"val": 0, "hex": "#1c1c1c"},
            "Marrón": {"val": 1, "hex": "#8B4513"},
            "Rojo": {"val": 2, "hex": "#FF0000"},
            "Naranja": {"val": 3, "hex": "#FFA500"},
            "Amarillo": {"val": 4, "hex": "#FFD700"},
            "Verde": {"val": 5, "hex": "#008000"},
            "Azul": {"val": 6, "hex": "#0000FF"},
            "Violeta": {"val": 7, "hex": "#8A2BE2"},
            "Gris": {"val": 8, "hex": "#808080"},
            "Blanco": {"val": 9, "hex": "#FFFFFF"}
        }
        
        self.lista_colores = list(self.colores_dict.keys())
        self.crear_interfaz()

    def crear_interfaz(self):
        # Título principal
        titulo = tk.Label(self.root, text="Simulador Gráfico de Resistencias", font=("Arial", 14, "bold"), bg="#f4f4f9", fg="#333")
        titulo.pack(pady=10)

        # --- SECCIÓN 1: CÓDIGO DE COLORES (GRÁFICO) ---
        frame_colores = tk.LabelFrame(self.root, text=" 1. Modo Gráfico: Determinar Colores ", font=("Arial", 10, "bold"), bg="#f4f4f9", padx=10, pady=10)
        frame_colores.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_colores, text="Valor en ohmios (ej. 160, 5800):", bg="#f4f4f9").pack(anchor="w")
        
        self.entry_valor = tk.Entry(frame_colores, font=("Arial", 11))
        self.entry_valor.pack(fill="x", pady=5)

        btn_grafico = tk.Button(frame_colores, text="Generar Gráfico y Colores", bg="#28a745", fg="white", font=("Arial", 10, "bold"), command=self.dibujar_resistencia)
        btn_grafico.pack(pady=5)

        # Lienzo (Canvas) para dibujar la resistencia visualmente
        self.canvas = tk.Canvas(frame_colores, width=380, height=100, bg="#e9ecef", highlightthickness=0)
        self.canvas.pack(pady=5)
        self.pintar_resistencia_inicial()

        self.lbl_detalles = tk.Label(frame_colores, text="Bandas: -", font=("Arial", 10, "italic"), bg="#f4f4f9", fg="#555")
        self.lbl_detalles.pack(anchor="w", pady=2)

        # --- SECCIÓN 2 y 3: CÁLCULOS EN SERIE Y PARALELO ---
        frame_calc = tk.LabelFrame(self.root, text=" 2 & 3. Circuitos en Serie y Paralelo ", font=("Arial", 10, "bold"), bg="#f4f4f9", padx=10, pady=10)
        frame_calc.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_calc, text="Cantidad de resistencias (n):", bg="#f4f4f9").pack(anchor="w")
        
        self.entry_n = tk.Entry(frame_calc, font=("Arial", 11))
        self.entry_n.pack(fill="x", pady=5)

        frame_botones = tk.Frame(frame_calc, bg="#f4f4f9")
        frame_botones.pack(fill="x", pady=5)

        btn_serie = tk.Button(frame_botones, text="Calcular Serie", bg="#007bff", fg="white", font=("Arial", 10, "bold"), command=self.calcular_serie)
        btn_serie.pack(side="left", expand=True, fill="x", padx=2)

        btn_paralelo = tk.Button(frame_botones, text="Calcular Paralelo", bg="#fd7e14", fg="white", font=("Arial", 10, "bold"), command=self.calcular_paralelo)
        btn_paralelo.pack(side="right", expand=True, fill="x", padx=2)

        self.lbl_resultado = tk.Label(frame_calc, text="Resultado: -", font=("Arial", 10), bg="#f4f4f9", fg="#333")
        self.lbl_resultado.pack(anchor="w", pady=5)

    def pintar_resistencia_inicial(self):
        self.canvas.delete("all")
        self.canvas.create_line(40, 50, 340, 50, width=6, fill="#6c757d") # Terminales
        self.canvas.create_oval(110, 15, 270, 85, fill="#d7ccc8", outline="#8d6e63", width=2) # Cuerpo

    def dibujar_resistencia(self):
        try:
            val_str = self.entry_valor.get().strip()
            if not val_str:
                messagebox.showerror("Error", "Ingresa un valor numérico.")
                return
            
            valor = int(val_str)
            if valor < 10:
                messagebox.showerror("Error", "El valor mínimo para este cálculo es 10 ohmios.")
                return

            s_val = str(valor)
            b1 = self.lista_colores[int(s_val[0])]
            b2 = self.lista_colores[int(s_val[1])]
            b3 = self.lista_colores[len(s_val) - 2]

            # Redibujar canvas con los colores correspondientes
            self.canvas.delete("all")
            self.canvas.create_line(40, 50, 340, 50, width=6, fill="#6c757d")
            self.canvas.create_oval(110, 15, 270, 85, fill="#d7ccc8", outline="#8d6e63", width=2)

            c1 = self.colores_dict[b1]["hex"]
            c2 = self.colores_dict[b2]["hex"]
            c3 = self.colores_dict[b3]["hex"]
            tolerancia = "#FFD700" # Dorado (5%)

            # Franjas de la resistencia
            self.canvas.create_rectangle(135, 17, 150, 83, fill=c1, outline="")
            self.canvas.create_rectangle(165, 15, 180, 85, fill=c2, outline="")
            self.canvas.create_rectangle(195, 16, 210, 84, fill=c3, outline="")
            self.canvas.create_rectangle(235, 15, 250, 85, fill=tolerancia, outline="")

            self.lbl_detalles.config(text=f"Bandas detectadas -> 1ª: {b1} | 2ª: {b2} | Multiplicador: {b3}")

        except (ValueError, IndexError):
            messagebox.showerror("Error", "Por favor ingresa un número entero válido.")

    def calcular_serie(self):
        try:
            n = int(self.entry_n.get())
            if n <= 0: raise ValueError()
            
            resistencias = [random.randint(10, 1000000000) for _ in range(n)]
            rts = sum(resistencias)
            self.lbl_resultado.config(text=f"[SERIE] Total ({n} resist.) = {rts:,.2f} Ω")
        except ValueError:
            messagebox.showerror("Error", "Ingresa una cantidad 'n' válida.")

    def calcular_paralelo(self):
        try:
            n = int(self.entry_n.get())
            if n <= 0: raise ValueError()
            
            resistencias = [random.randint(10, 1000000000) for _ in range(n)]
            suma_inversos = sum(1.0 / r for r in resistencias)
            rtp = 1.0 / suma_inversos
            self.lbl_resultado.config(text=f"[PARALELO] Total ({n} resist.) = {rtp:,.2f} Ω")
        except ValueError:
            messagebox.showerror("Error", "Ingresa una cantidad 'n' válida.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResistenciaApp(root)
    root.mainloop()