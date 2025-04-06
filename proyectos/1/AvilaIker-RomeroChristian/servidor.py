#Versión 5.0

import threading
import time
import random
import queue

class Servidor: #Clase que representa al servidor
    def __init__(self, max_conexiones = 3, limite_premium_seguidos = 2): # Constructor de la clase
        self.jugadores_conectados = [] # Lista para almacenar los jugadores conectados
        self.lock = threading.Lock() # Lock para sincronizar el acceso a la lista de jugadores conectados
        self.semaforo = threading.Semaphore(max_conexiones) # Semaforo para limitar el número de conexiones simultaneas
        self.cola_espera = queue.Queue() # Cola de espera para los jugadores
        self.limite_premium = limite_premium_seguidos # Límite de jugadores premium seguidos
        self.premium_seguidos = 0 # Contador de jugadores premium seguidos

    def agregar_a_cola(self, jugador): # Método para agregar un jugador a la cola de espera
        prioridad = 0 if jugador.es_premium else 1 # Asigna una prioridad al jugador según su tipo (premium o no)
        self.cola_espera.put((prioridad, jugador.id_jugador, jugador)) # Agrega el jugador a la cola de espera
        print(f"[Servidor] Jugador {jugador.id_jugador} agregado a la cola (Premium: {jugador.es_premium})")

    
    def procesar_conexiones(self): # Método para procesar la conexión de un jugador
        while not self.cola_espera.empty(): # Mientras haya jugadores en la cola de espera
            siguiente = self._siguiente_jugador_justo()
            if siguiente:
                prioridad, id_jugador, jugador = siguiente
                self.semaforo.acquire() # Adquiere el semáforo para limitar el número de conexiones simultaneas
                threading.Thread(target=self._atender_jugador, args=(jugador,)).start() # Crea un hilo para atender al jugador
            else:
                time.sleep(0.1)

    def _siguiente_jugador_justo(self): # Devuelve el siguiente jugador a atender, aplicando la política de justicia:
                                        # Si hay muchos premium seguidos, se atiende a un jugador normal, si hay alguno.
        temporales = [] # Lista para almacenar los jugadores temporalmente
        jugador_normal_encontrado = None # Variable para almacenar el jugador normal si es encontrado

        while not self.cola_espera.empty(): # Mientras haya jugadores en la cola de espera
            item = self.cola_espera.get() # Obtiene el siguiente jugador de la cola de espera
            prioridad, id_jugador, jugador = item # Desempaqueta los datos del jugador

            if self.premium_seguidos >= self.limite_premium and prioridad == 1: # Si hay muchos premium seguidos y el jugador es normal
                jugador_normal_encontrado = item # Almacena el jugador normal
                break # Sale del bucle
            else: # Si no, agrega el jugador a la lista temporal
                temporales.append(item)

        for item in temporales: # Vuelve a agregar los jugadores temporales a la cola de espera
            self.cola_espera.put(item) # Agrega el jugador a la cola de espera

        if jugador_normal_encontrado: # Si se encontró un jugador normal, se atiende primero
            self.premium_seguidos = 0 # Reinicia el contador de jugadores premium seguidos
            return jugador_normal_encontrado

        if temporales: # Si hay jugadores en la lista temporal, se atiende el primero
            primero = self.cola_espera.get() # Obtiene el siguiente jugador de la cola de espera
            if primero[0] == 0: # Si el jugador es premium, incrementa el contador de jugadores premium seguidos
                self.premium_seguidos += 1
            else: # Si el jugador es normal, reinicia el contador de jugadores premium seguidos
                self.premium_seguidos = 0
            return primero

        return None # Si no hay jugadores en la cola de espera, devuelve None
    
    def _atender_jugador(self, jugador): # Método para atender a un jugador
        print(f"[Servidor] Atendiendo a Jugador {jugador.id_jugador} (Premium: {jugador.es_premium})")
        time.sleep(random.uniform(0.5, 1.5)) # Simula el tiempo de atención al jugador
        
        with self.lock: # Bloquea el acceso a la lista de jugadores conectados
            self.jugadores_conectados.append(jugador.id_jugador) # Agrega el jugador a la lista de jugadores conectados
            print(f"[Servidor] Jugador {jugador.id_jugador} conectado exitosamente.")
            
        self.semaforo.release() # Libera el semáforo
