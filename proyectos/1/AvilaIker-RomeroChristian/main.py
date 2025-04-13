#Bibliotecas
import threading
import random
import time
import tkinter as tk
from tkinter import scrolledtext

#Constantes
MAX_JUGADORES_EN_SERVIDOR = 12 #Limite de jugadores
OBJETIVOS_DEPENDENCIAS = { #Establecemos las relaciones entre las zonas de captura
    "A": [],
    "B": [],
    "C": ["A", "B"],
    "D": [],
    "E": [],
    "F": ["D", "E"],
    "G": ["C", "F"]
}

#Clase jugador
class Jugador:
    def __init__(self, id):
        self.id = id
        self.destreza = round(random.uniform(0.5, 2.0), 2) # Le asignamos un nivel de habilidad a cada jugador
        self.tiempo_restante = random.randint(15, 45) # Tiempo que puede estar dentro del servidor
        self.objetivo_actual = None # Objetivo que va a estar capturando

    def __str__(self):
        return f"Jugador {self.id} (🌟{self.destreza}, ⏱️{self.tiempo_restante})"


# Clase del Servidor
class SimulacionServidor:
    def __init__(self, gui):
        self.gui = gui
        self.lock = threading.RLock() # RLock para sincronizar el acceso a los recursos compartidos usando llamadas anidadas
        self.semaforo_servidor = threading.Semaphore(MAX_JUGADORES_EN_SERVIDOR) # Semaforo para limitar el numero de jugadores en el servidor
        self.jugadores_cola = [] # Lista de jugadores en cola
        self.jugadores_servidor = [] # Dentro de la partida
        self.objetivos = {k: 0 for k in OBJETIVOS_DEPENDENCIAS} # Estado de los objetivos
        self.estado_partida = "EN_CURSO"
        self.jugador_id_counter = 1 # Contador para asignar IDs unicos a los jugadores
        self.running = False  # Indica si la simulacion esta corriendo
        self.reiniciando = False # Bandera para controlar el estado de reinicio de partida

    def iniciar_simulacion(self): # Iniciamos la simulacion principal
        if not self.running:
            self.running = True
            threading.Thread(target=self.bucle_simulacion, daemon=True).start()
            self.gui.log_event("🟢 Simulacion iniciada.")

    def bucle_simulacion(self): # Bucle principal de la simulacion
        try:
            # Agregamos los 24 jugadores a la simulacion 
            for _ in range(24):
                self.agregar_jugador_cola()

            contador_minutos = 0
            while self.running:
                if not self.reiniciando:
                    # Cada 4 minutos se agrega un nuevo jugador
                    if contador_minutos % 4 == 0:  
                        self.agregar_jugador_cola()

                    self.intentar_conectar_jugadores()
                    self.actualizar_estado_jugadores()
                    
                    # Actualizar GUI fuera del lock para evitar bloqueos
                    with self.lock:
                        jugadores_cola = self.jugadores_cola.copy()
                        estado_servidor = self.generar_estado_servidor()
                    
                    self.gui.update_queue(jugadores_cola)
                    self.gui.update_server(estado_servidor)
                
                time.sleep(1)  # Cada iteracion representa 1 minuto
                contador_minutos += 1
        except Exception as e:
            self.gui.log_event(f"🔴 Error en bucle_simulacion: {str(e)}")

    def agregar_jugador_cola(self): # Añade un nuevo jugador a la cola de espera
        with self.lock:
            try:
                jugador = Jugador(self.jugador_id_counter)
                self.jugador_id_counter += 1
                self.jugadores_cola.append(jugador)
                self.gui.log_event(f"🎮 {jugador} se unió a la cola.")
            except Exception as e:
                self.gui.log_event(f"🔴 Error al agregar jugador: {str(e)}")

    def intentar_conectar_jugadores(self): # Mueve jugadores de la cola al servidor si hay espacio
        with self.lock:
            try:
                while self.jugadores_cola and self.semaforo_servidor._value > 0:
                    jugador = self.jugadores_cola.pop(0)
                    self.semaforo_servidor.acquire()  # Decrementa el semaforo
                    self.jugadores_servidor.append(jugador)
                    self.gui.log_event(f"✅ {jugador} entró al servidor.")
            except Exception as e:
                self.gui.log_event(f"🔴 Error al conectar jugadores: {str(e)}")

    def actualizar_estado_jugadores(self): # Actualiza el estado de los jugadores y objetivos
        if self.reiniciando:
            return
        
        with self.lock:
            try:
                jugadores_desconectados = []
                for jugador in self.jugadores_servidor:
                    try:
                        # Asigna un nuevo objetivo si no tiene o si el actual esta completado
                        if jugador.objetivo_actual is None or self.objetivos.get(jugador.objetivo_actual, 100) >= 100:
                            jugador.objetivo_actual = self.elegir_objetivo_disponible()
                        
                        # Procesa la captura del objetivo
                        if jugador.objetivo_actual and jugador.objetivo_actual in self.objetivos:
                            progreso = jugador.destreza
                            self.objetivos[jugador.objetivo_actual] += progreso
                            if self.objetivos[jugador.objetivo_actual] >= 100:
                                self.objetivos[jugador.objetivo_actual] = 100
                                self.gui.log_event(f"🏁 Objetivo {jugador.objetivo_actual} capturado por {jugador}.")
                        
                        # Reduce el tiempo de conexion del jugador
                        jugador.tiempo_restante -= 1
                        if jugador.tiempo_restante <= 0:
                            jugadores_desconectados.append(jugador)
                            self.gui.log_event(f"🔌 {jugador} se desconectó por tiempo agotado.")
                    
                    except Exception as e:
                        self.gui.log_event(f"🔴 Error al actualizar jugador {jugador.id}: {str(e)}")

                # Elimina jugadores que agotaron su tiempo
                for jugador in jugadores_desconectados:
                    try:
                        self.jugadores_servidor.remove(jugador)
                        self.semaforo_servidor.release()  # Libera espacio en el semaforo
                    except Exception as e:
                        self.gui.log_event(f"🔴 Error al desconectar jugador: {str(e)}")
                
                # Verifica si se completo el objetivo final (G)
                if self.objetivos["G"] >= 100:
                    self.terminar_partida()
            
            except Exception as e:
                self.gui.log_event(f"🔴 Error en actualizar_estado_jugadores: {str(e)}")

    def elegir_objetivo_disponible(self): # Selecciona un objetivo valido para el jugador
        with self.lock:
            try:
                disponibles = []
                for objetivo, deps in OBJETIVOS_DEPENDENCIAS.items():
                    # Verifica dependencias para el objetivo G
                    if objetivo == "G" and not all(self.objetivos[d] >= 100 for d in deps):
                        continue
                    # Verifica si el objetivo no esta completado y sus dependencias estan al 100
                    if self.objetivos[objetivo] < 100 and all(self.objetivos[d] >= 100 for d in deps):
                        disponibles.append(objetivo)
                return random.choice(disponibles) if disponibles else None
            except Exception as e:
                self.gui.log_event(f"🔴 Error al elegir objetivo: {str(e)}")
                return None

    def terminar_partida(self): # Finaliza la partida y reinicia el estado del servidor
        with self.lock:
            try:
                self.reiniciando = True 
                self.gui.log_event("🎉 Objetivo final G capturado. Fin de la partida.")
                self.gui.log_event("🔁 Reiniciando partida y desconectando jugadores...")
                
                # Limpia los objetivos de los jugadores
                for jugador in self.jugadores_servidor:
                    jugador.objetivo_actual = None
                
                time.sleep(2)  # Pequeña pausa para el reinicio que soluciona algunos errores
                self.objetivos = {k: 0 for k in OBJETIVOS_DEPENDENCIAS}  # Reinicia todos los objetivos
                self.jugadores_cola.extend(self.jugadores_servidor)  # Devuelve jugadores a la cola
                self.jugadores_servidor.clear()
                
                # Restablece el semaforo al valor maximo
                while self.semaforo_servidor._value < MAX_JUGADORES_EN_SERVIDOR:
                    self.semaforo_servidor.release()
                
                self.reiniciando = False
            except Exception as e:
                self.gui.log_event(f"🔴 Error al terminar partida: {str(e)}")
                self.reiniciando = False

    def generar_estado_servidor(self): # Genera el estado actual del servidor para mostrar en GUI
        with self.lock:
            lineas = [f"{k}: {v:.0f}%" for k, v in self.objetivos.items()]
            lineas.append("\nJugadores conectados:")
            for j in self.jugadores_servidor:
                punto = j.objetivo_actual if j.objetivo_actual else "..."
                lineas.append(f"{j} ➤ Objetivo: {punto}")
            return lineas

# Interfaz Grafica (GUI)
class GameServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulación de Servidor de Videojuego Cooperativo")
        self.master.configure(bg="black")

        # Configuracion de colores y fuentes
        self.fg_color = "lime"
        self.bg_color = "black"
        self.font = ("Courier", 10)

        # Frame principal
        self.main_frame = tk.Frame(master, bg=self.bg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configurar pesos de filas y columnas para redimensionamiento
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

        # Crear los tres paneles principales
        self.queue_frame = self.create_labeled_frame("Cola")
        self.queue_text = self.create_text_area(self.queue_frame)

        self.server_frame = self.create_labeled_frame("Servidor")
        self.server_text = self.create_text_area(self.server_frame)

        self.history_frame = self.create_labeled_frame("Historial")
        self.history_text = self.create_text_area(self.history_frame)

        # Colocar los frames usando grid
        self.queue_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.server_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.history_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # Boton de inicio
        self.start_button = tk.Button(
            master,
            text="Iniciar Simulación",
            command=self.iniciar_simulacion,
            bg="gray20",
            fg=self.fg_color,
            font=("Courier", 12, "bold")
        )
        self.start_button.grid(row=1, column=0, columnspan=3, pady=10)

        # Instancia de la simulacion
        self.simulacion = SimulacionServidor(self)

    def create_labeled_frame(self, title): # Crea un frame con titulo estilizado
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
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        return frame

    def create_text_area(self, parent): # Crea un area de texto con scroll
        text_widget = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=self.font,
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            height=20
        )
        text_widget.grid(row=0, column=0, sticky="nsew")
        text_widget.config(state=tk.DISABLED)
        return text_widget

    def log_event(self, message): # Registra un evento en el historial
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, message + "\n")
        self.history_text.see(tk.END)  # Auto-scroll al final
        self.history_text.config(state=tk.DISABLED)

    def update_queue(self, jugadores): # Actualiza el panel de cola de jugadores
        self.queue_text.config(state=tk.NORMAL)
        self.queue_text.delete(1.0, tk.END)
        for j in jugadores:
            self.queue_text.insert(tk.END, f"{j}\n")
        self.queue_text.see(tk.END)  # Auto-scroll
        self.queue_text.config(state=tk.DISABLED)

    def update_server(self, estado): # Actualiza el panel de estado del servidor
        self.server_text.config(state=tk.NORMAL)
        self.server_text.delete(1.0, tk.END)
        for linea in estado:
            self.server_text.insert(tk.END, linea + "\n")
        self.server_text.see(tk.END)  # Auto-scroll
        self.server_text.config(state=tk.DISABLED)

    def iniciar_simulacion(self): # Inicia la simulacion al presionar el boton
        self.simulacion.iniciar_simulacion()

#Main
if __name__ == "__main__":
    root = tk.Tk()
    app = GameServerGUI(root)
    root.mainloop()