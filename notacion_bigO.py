import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Constantes ---
# El valor máximo para 'n' y para los ejes del gráfico.
SLIDER_MAX = 50
PLOT_MAX = 50
SLIDER_MIN = 2

# Usamos un diccionario con las complejidades solicitadas.
# Las funciones ahora usan NumPy para operar sobre arrays de datos.
COMPLEXITIES = {
    "O(1) - Constante": {
        "func": lambda n: np.ones_like(n),
        "color": "cyan"
    },
    "O(log n) - Logarítmica": {
        "func": lambda n: np.log2(n), # Usamos log base 2, común en computación
        "color": "green"
    },
    "O(n) - Lineal": {
        "func": lambda n: n,
        "color": "blue"
    },
    "O(n^2) - Cuadrática": {
        "func": lambda n: n**2,
        "color": "red"
    }
}


class BigOVisualizer:
    """
    Clase principal para la aplicación de visualización de Big O con Matplotlib.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Visualizador de Complejidad Big O con Matplotlib")
        self.master.geometry("1000x700")
        self.master.resizable(False, False)

        # Frame principal
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Configuración de Matplotlib ---
        self.fig = Figure(dpi=100)
        self.ax = self.fig.add_subplot(111)

        # 1. Configurar ejes y etiquetas una sola vez
        self.ax.set_title("Crecimiento de Notación Big O", fontsize=16)
        self.ax.set_xlabel("Tamaño de la entrada (n)", fontsize=12)
        self.ax.set_ylabel("Número de operaciones", fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_xlim(0, PLOT_MAX)
        self.ax.set_ylim(0, PLOT_MAX)

        # 2. Pre-calcular todos los datos y crear los objetos de línea
        self.lines = {}
        # Generamos un array de puntos x para una curva suave
        self.x_data = np.linspace(1, SLIDER_MAX, num=500)
        # np.log2(1) es 0, pero para evitar problemas con linspace empezando en 0, aseguramos que sea > 0
        self.x_data[self.x_data < 1] = 1

        for name, props in COMPLEXITIES.items():
            y_data = props["func"](self.x_data)
            # Creamos la línea vacía y la guardamos junto a sus datos completos
            line, = self.ax.plot([], [], label=name, color=props["color"], linewidth=2.5)
            self.lines[name] = {'line': line, 'y_data': y_data}

        self.ax.legend(loc="upper left")

        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame para los controles
        controls_frame = ttk.Frame(main_frame, padding="10")
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Checkboxes para visibilidad ---
        visibility_frame = ttk.LabelFrame(controls_frame, text="Funciones Visibles")
        visibility_frame.pack(pady=20, padx=5, fill=tk.X)

        self.visibility_vars = {}
        for name in COMPLEXITIES.keys():
            var = tk.BooleanVar(value=False)
            self.visibility_vars[name] = var
            cb = ttk.Checkbutton(
                visibility_frame,
                text=name,
                variable=var,
                command=self._toggle_line_visibility)
            cb.pack(anchor='w', padx=5, pady=2)

        # Deslizador para 'n'
        ttk.Label(controls_frame, text="Valor de 'n'").pack(pady=(0, 5))
        self.n_var = tk.IntVar(value=SLIDER_MIN)
        self.slider = ttk.Scale(
            controls_frame,
            from_=SLIDER_MAX,
            to=SLIDER_MIN,
            orient=tk.VERTICAL,
            variable=self.n_var,
            command=self.update_plot,
            length=400
        )
        self.slider.pack(pady=10, fill=tk.Y, expand=True)

        self.n_label = ttk.Label(controls_frame, text=f"n = {self.n_var.get()}", font=("Helvetica", 12))
        self.n_label.pack(pady=5)

        # 3. Dibujar el estado inicial del gráfico
        self.update_plot(self.n_var.get())

    def _toggle_line_visibility(self):
        """
        Actualiza la visibilidad de cada línea en el gráfico según el estado
        de su checkbox correspondiente.
        """
        for name, data in self.lines.items():
            is_visible = self.visibility_vars[name].get()
            data['line'].set_visible(is_visible)
        self.canvas.draw_idle()

    def update_plot(self, n_value):
        """
        Actualiza los datos de las líneas del gráfico hasta el valor 'n' actual,
        sin redibujar todo el gráfico.
        """
        n = int(float(n_value))
        self.n_var.set(n)
        self.n_label.config(text=f"n = {n}")

        # Encontrar los índices de nuestros datos pre-calculados que corresponden a x <= n
        indices_to_draw = np.where(self.x_data <= n)[0]

        # Actualizar los datos de cada línea con el tramo correspondiente
        for name, data in self.lines.items():
            line = data['line']
            y_data = data['y_data']

            if len(indices_to_draw) > 0:
                # Obtenemos el último índice a dibujar
                end_index = indices_to_draw[-1] + 1
                line.set_data(self.x_data[:end_index], y_data[:end_index])
            else:
                # Si no hay índices (n < 1), la línea está vacía
                line.set_data([], [])

        # Redibujar el canvas de forma eficiente
        self.canvas.draw_idle()

def main():
    """Función principal para iniciar la aplicación."""
    root = tk.Tk()
    BigOVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# Actividad pedagógica 

# Ejecuten el programa.
# Aumenten progresivamente los valores de n.
# Tomen captura de la gráfica.
# Respondan:
# ¿Cuál curva crece más rápido?
# ¿Cuál casi no cambia?
# ¿Por qué O(n²) se vuelve inviable rápidamente?