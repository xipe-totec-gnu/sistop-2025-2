import tkinter as tk
from queue import Queue, Empty

class ReservaGUI:
    """
    Interfaz gráfica con tkinter para:
      - Mostrar la disponibilidad de canchas/horarios (con colores según la prioridad).
      - Mostrar el log de acciones en tiempo real.
      - Mostrar las estadísticas de reservas exitosas.
    """

    def __init__(self, root, sistema_reservas, update_interval=1000):
        """
        :param root: ventana raíz de tkinter
        :param sistema_reservas: instancia de SistemaReservas
        :param update_interval: frecuencia (ms) para actualizar la vista
        """
        self.root = root
        self.sistema = sistema_reservas
        self.update_interval = update_interval

        self.root.title("Sistema de Reservas de Canchas")

        # Frame superior: contenedor para la grilla de canchas
        frame_top = tk.Frame(self.root)
        frame_top.pack(side=tk.TOP, padx=5, pady=5)

        # Creamos la cuadrícula de etiquetas
        self.labels = []
        for i in range(self.sistema.num_canchas):
            fila_lbl = []
            for j in range(self.sistema.num_horarios):
                lbl = tk.Label(
                    frame_top,
                    text="Libre",
                    width=12,
                    borderwidth=1,
                    relief="solid"
                )
                lbl.grid(row=i, column=j, padx=4, pady=4)
                fila_lbl.append(lbl)
            self.labels.append(fila_lbl)

        # Frame central: Log de acciones
        frame_middle = tk.Frame(self.root)
        frame_middle.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tk.Label(frame_middle, text="Registro de acciones en tiempo real:").pack(anchor="w")

        # Texto para mostrar logs
        self.log_text = tk.Text(frame_middle, height=10, width=60)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Frame inferior: estadísticas
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(frame_bottom, text="Estadísticas de Reservas:").pack(anchor="w")
        self.stats_label = tk.Label(frame_bottom, text="(Aquí se mostrarán las estadísticas)")
        self.stats_label.pack(anchor="w")

        # Colocamos la log_queue en el sistema
        self.log_queue = Queue()
        self.sistema.set_log_queue(self.log_queue)

        # Iniciamos las actualizaciones periódicas
        self.actualizar_estado()
        self.actualizar_logs()
        self.actualizar_stats()

    def actualizar_estado(self):
        """
        Actualiza la cuadrícula de canchas, coloreando según la prioridad.
        """
        self.sistema.lock_canchas.acquire()
        try:
            for i in range(self.sistema.num_canchas):
                for j in range(self.sistema.num_horarios):
                    actual = self.sistema.estado_canchas[i][j]
                    if actual is None:
                        txt = "Libre"
                        bg_color = "white"
                    else:
                        user_id, prio = actual
                        txt = f"U:{user_id}\nP:{prio}"
                        if prio == 2:
                            bg_color = "#ffcccc"  
                        else:
                            bg_color = "#ccffff"  
                    lbl = self.labels[i][j]
                    lbl.config(text=txt, bg=bg_color)
        finally:
            self.sistema.lock_canchas.release()

        # Reprogramamos la actualización
        self.root.after(self.update_interval, self.actualizar_estado)

    def actualizar_logs(self):
        """
        Extrae nuevos mensajes de la cola de logs y los añade a la ventana de texto.
        """
        try:
            while True:  # Vaciar la cola
                mensaje = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, mensaje + "\n")
                self.log_text.see(tk.END)  # Autoscroll
        except Empty:
            pass

        # Reprogramamos la siguiente lectura de la cola
        self.root.after(500, self.actualizar_logs)

    def actualizar_stats(self):
        """
        Actualiza la etiqueta con las estadísticas de reservas exitosas.
        """
        stats_str = self.sistema.get_stats_string()
        self.stats_label.config(text=stats_str)

        # Repetimos cada cierto tiempo
        self.root.after(1000, self.actualizar_stats)
