import threading
import random
import time
import tkinter as tk
from tkinter import scrolledtext

# ====================
# === Configuración ===
# ====================
MAX_JUGADORES_EN_SERVIDOR = 12
OBJETIVOS_DEPENDENCIAS = {
    "A": [],
    "B": [],
    "C": ["A", "B"],
    "D": [],
    "E": [],
    "F": ["D", "E"],
    "G": ["C", "F"]
}

# =====================
# === Jugador Clase ===
# =====================
class Jugador:
    def __init__(self, id):
        self.id = id
        self.destreza = round(random.uniform(0.5, 2.0), 2)
        self.tiempo_restante = random.randint(15, 45)
        self.objetivo_actual = None

    def __str__(self):
        return f"Jugador {self.id} (🌟{self.destreza}, ⏱️{self.tiempo_restante})"

# ================================
# === Lógica del Servidor Clase ===
# ================================
class SimulacionServidor:
    def __init__(self, gui):
        self.gui = gui
        self.lock = threading.Lock()
        self.semaforo_servidor = threading.Semaphore(MAX_JUGADORES_EN_SERVIDOR)
        self.jugadores_cola = []
        self.jugadores_servidor = []
        self.objetivos = {k: 0 for k in OBJETIVOS_DEPENDENCIAS}
        self.estado_partida = "EN_CURSO"
        self.jugador_id_counter = 1
        self.running = False

    def iniciar_simulacion(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.bucle_simulacion, daemon=True).start()
            self.gui.log_event("🟢 Simulación iniciada.")

    def bucle_simulacion(self):
        for _ in range(24):
            self.agregar_jugador_cola()

        contador_minutos = 0
        while self.running:
            if contador_minutos % 4 == 0:
                self.agregar_jugador_cola()

            self.intentar_conectar_jugadores()
            self.actualizar_estado_jugadores()
            self.gui.update_queue(self.jugadores_cola)
            self.gui.update_server(self.generar_estado_servidor())

            time.sleep(1)
            contador_minutos += 1

    def agregar_jugador_cola(self):
        with self.lock:
            jugador = Jugador(self.jugador_id_counter)
            self.jugador_id_counter += 1
            self.jugadores_cola.append(jugador)
            self.gui.log_event(f"🎮 {jugador} se unió a la cola.")

    def intentar_conectar_jugadores(self):
        with self.lock:
            while self.jugadores_cola and self.semaforo_servidor._value > 0:
                jugador = self.jugadores_cola.pop(0)
                self.semaforo_servidor.acquire()
                self.jugadores_servidor.append(jugador)
                self.gui.log_event(f"✅ {jugador} entró al servidor.")

    def actualizar_estado_jugadores(self):
        jugadores_desconectados = []
        for jugador in self.jugadores_servidor:
            if jugador.objetivo_actual is None or self.objetivos.get(jugador.objetivo_actual, 100) >= 100:
                jugador.objetivo_actual = self.elegir_objetivo_disponible()

            if jugador.objetivo_actual:
                progreso = jugador.destreza
                self.objetivos[jugador.objetivo_actual] += progreso
                if self.objetivos[jugador.objetivo_actual] >= 100:
                    self.objetivos[jugador.objetivo_actual] = 100
                    self.gui.log_event(f"🏁 Objetivo {jugador.objetivo_actual} capturado por {jugador}.")

            jugador.tiempo_restante -= 1
            if jugador.tiempo_restante <= 0:
                jugadores_desconectados.append(jugador)
                self.gui.log_event(f"🔌 {jugador} se desconectó por tiempo agotado.")

        for jugador in jugadores_desconectados:
            self.jugadores_servidor.remove(jugador)
            self.semaforo_servidor.release()

        if self.objetivos["G"] >= 100:
            self.terminar_partida()

    def elegir_objetivo_disponible(self):
        disponibles = []
        for objetivo, deps in OBJETIVOS_DEPENDENCIAS.items():
            if self.objetivos[objetivo] < 100 and all(self.objetivos[d] >= 100 for d in deps):
                disponibles.append(objetivo)
        return random.choice(disponibles) if disponibles else None


    def terminar_partida(self):
        self.gui.log_event("🎉 Objetivo final G capturado. Fin de la partida.")
        self.gui.log_event("🔁 Reiniciando partida y desconectando jugadores...")
        self.objetivos = {k: 0 for k in OBJETIVOS_DEPENDENCIAS}
        self.jugadores_cola += self.jugadores_servidor
        self.jugadores_servidor.clear()
        while self.semaforo_servidor._value < MAX_JUGADORES_EN_SERVIDOR:
            self.semaforo_servidor.release()

    def generar_estado_servidor(self):
        lineas = [f"{k}: {v:.0f}%" for k, v in self.objetivos.items()]
        lineas.append("\nJugadores conectados:")
        for j in self.jugadores_servidor:
            punto = j.objetivo_actual if j.objetivo_actual else "..."
            lineas.append(f"{j} ➤ Objetivo: {punto}")
        return lineas

# ================================
# === Interfaz Gráfica (GUI) ===
# ================================
class GameServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulación de Servidor de Videojuego Cooperativo")
        self.master.configure(bg="black")

        self.fg_color = "lime"
        self.bg_color = "black"
        self.font = ("Courier", 10)

        self.main_frame = tk.Frame(master, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.queue_frame = self.create_labeled_frame("Cola")
        self.queue_text = self.create_text_area(self.queue_frame)

        self.server_frame = self.create_labeled_frame("Servidor")
        self.server_text = self.create_text_area(self.server_frame)

        self.history_frame = self.create_labeled_frame("Historial")
        self.history_text = self.create_text_area(self.history_frame)

        self.queue_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.server_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.history_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.start_button = tk.Button(
            master,
            text="Iniciar Simulación",
            command=self.iniciar_simulacion,
            bg="gray20",
            fg=self.fg_color,
            font=("Courier", 12, "bold")
        )
        self.start_button.pack(pady=10)

        self.simulacion = SimulacionServidor(self)

    def create_labeled_frame(self, title):
        frame = tk.LabelFrame(
            self.main_frame,
            text=title,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Courier", 12, "bold"),
            bd=2,
            relief=tk.GROOVE,
            labelanchor="n"
        )
        return frame

    def create_text_area(self, parent):
        text_widget = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=self.font,
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            height=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.config(state=tk.DISABLED)
        return text_widget

    def log_event(self, message):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, message + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)

    def update_queue(self, jugadores):
        self.queue_text.config(state=tk.NORMAL)
        self.queue_text.delete(1.0, tk.END)
        for j in jugadores:
            self.queue_text.insert(tk.END, f"{j}\n")
        self.queue_text.config(state=tk.DISABLED)

    def update_server(self, estado):
        self.server_text.config(state=tk.NORMAL)
        self.server_text.delete(1.0, tk.END)
        for linea in estado:
            self.server_text.insert(tk.END, linea + "\n")
        self.server_text.config(state=tk.DISABLED)

    def iniciar_simulacion(self):
        self.simulacion.iniciar_simulacion()

# =====================
# === Ejecutar GUI ===
# =====================
if __name__ == "__main__":
    root = tk.Tk()
    app = GameServerGUI(root)
    root.mainloop()

