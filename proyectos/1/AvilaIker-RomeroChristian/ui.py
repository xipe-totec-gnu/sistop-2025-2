import tkinter as tk
from tkinter import ttk

class Interfaz:
    def __init__(self, root, servidor):
        self.root = root
        self.servidor = servidor
        self.root.title("Simulación de Servidor de Videojuego")
        self.root.geometry("800x600")

        self.frame_botones = tk.Frame(root)
        self.frame_botones.pack(pady=10)

        self.boton_iniciar = tk.Button(self.frame_botones, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.boton_iniciar.pack()

        self.frame_main = tk.Frame(root)
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        self.text_cola = self._crear_text_widget("Jugadores en Cola")
        self.text_conectados = self._crear_text_widget("Jugadores Conectados")
        self.text_historial = self._crear_text_widget("Historial de Eventos", height=15)

        self.jugadores = []
        self.contador_jugadores = 1

    def _crear_text_widget(self, titulo, height=10):
        frame = tk.LabelFrame(self.frame_main, text=titulo)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_widget = tk.Text(frame, height=height)
        text_widget.pack(fill=tk.BOTH, expand=True)
        return text_widget

    def iniciar_simulacion(self):
        self.jugadores.clear()
        for _ in range(24):
            self._nuevo_jugador()

        self.servidor.procesar_conexiones(self.agregar_evento, self.actualizar_ui)

        # Generar nuevos jugadores cada 30 segundos
        self._agregar_periodicamente()

    def _nuevo_jugador(self):
        import random
        from jugador import Jugador
        jugador = Jugador(self.contador_jugadores, es_vip=random.random() < 0.3)
        self.contador_jugadores += 1
        self.jugadores.append(jugador)
        self.servidor.agregar_jugador(jugador)
        self.agregar_evento(f"Jugador {jugador.id} agregado a la cola. (VIP: {jugador.es_vip})")
        self.actualizar_ui()

    def _agregar_periodicamente(self):
        self._nuevo_jugador()
        self.root.after(30000, self._agregar_periodicamente)

    def agregar_evento(self, texto):
        self.text_historial.insert(tk.END, texto + "\n")
        self.text_historial.see(tk.END)

    def actualizar_ui(self):
        self.text_cola.delete(1.0, tk.END)
        self.text_conectados.delete(1.0, tk.END)

        cola_list = list(self.servidor.cola_espera.queue)
        for prioridad, _, jugador in sorted(cola_list, key=lambda x: (x[0], x[1])):
            self.text_cola.insert(tk.END, f"{jugador.id} (VIP: {jugador.es_vip})\n")

        for jugador in self.servidor.jugadores_conectados:
            self.text_conectados.insert(
                tk.END,
                f"{jugador.id} | Kills: {jugador.kills} | KD: {jugador.kd:.2f} | $: {jugador.monedas}\n"
            )
