import threading
import queue

class Servidor:
    def __init__(self, max_conexiones=12, max_vip_seguidos=3):
        self.cola_espera = queue.PriorityQueue()
        self.jugadores_conectados = []
        self.lock = threading.Lock()
        self.semaforo = threading.Semaphore(max_conexiones)
        self.vip_seguidos = 0
        self.max_vip_seguidos = max_vip_seguidos

    def agregar_jugador(self, jugador):
        prioridad = 0 if jugador.es_vip else 1
        self.cola_espera.put((prioridad, jugador.id, jugador))

    def procesar_conexiones(self, actualizar_historial, actualizar_ui):
        def ciclo():
            while True:
                if not self.cola_espera.empty():
                    jugador = self._obtener_siguiente()
                    if jugador:
                        self.semaforo.acquire()
                        with self.lock:
                            jugador.conectado = True
                            self.jugadores_conectados.append(jugador)
                        actualizar_historial(f"Jugador {jugador.id} conectado. (VIP: {jugador.es_vip})")
                        actualizar_ui()

                        hilo = threading.Thread(
                            target=jugador.jugar,
                            args=(self, actualizar_historial, actualizar_ui),
                            daemon=True
                        )
                        hilo.start()
                else:
                    time.sleep(1)
        threading.Thread(target=ciclo, daemon=True).start()

    def _obtener_siguiente(self):
        temporales = []
        jugador_normal = None

        while not self.cola_espera.empty():
            prioridad, _, jugador = self.cola_espera.get()
            if self.vip_seguidos >= self.max_vip_seguidos and prioridad == 1:
                jugador_normal = jugador
                break
            else:
                temporales.append((prioridad, jugador.id, jugador))

        for item in temporales:
            self.cola_espera.put(item)

        if jugador_normal:
            self.vip_seguidos = 0
            return jugador_normal

        if not self.cola_espera.empty():
            prioridad, _, jugador = self.cola_espera.get()
            if prioridad == 0:
                self.vip_seguidos += 1
            else:
                self.vip_seguidos = 0
            return jugador

        return None

    def desconectar_jugador(self, jugador):
        with self.lock:
            if jugador in self.jugadores_conectados:
                self.jugadores_conectados.remove(jugador)
                jugador.conectado = False
        self.semaforo.release()

