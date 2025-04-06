#Versión 4.0

import threading
import time
import random
import queue

class Servidor: #Clase que representa al servidor
    def __init__(self, max_conexiones = 3): # Constructor de la clase
        self.jugadores_conectados = [] # Lista para almacenar los jugadores conectados
        self.lock = threading.Lock() # Lock para sincronizar el acceso a la lista de jugadores conectados
        self.semaforo = threading.Semaphore(max_conexiones) # Semaforo para limitar el número de conexiones simultaneas
        self.cola_espera = queue.Queue() # Cola de espera para los jugadores

    def agregar_a_cola(self, jugador): # Método para agregar un jugador a la cola de espera
        prioridad = 0 if jugador.es_premium else 1 # Asigna una prioridad al jugador según su tipo (premium o no)
        self.cola_espera.put((prioridad, jugador.id_jugador, jugador)) # Agrega el jugador a la cola de espera
        print(f"[Servidor] Jugador {jugador.id_jugador} agregado a la cola (Premium: {jugador.es_premium})")

    
    def procesar_conexiones(self): # Método para procesar la conexión de un jugador
        while not self.cola_espera.empty(): # Mientras haya jugadores en la cola de espera
            prioridad, id_jugador, jugador = self.cola_espera.get() # Obtiene el siguiente jugador de la cola de espera

            self.semaforo.acquire() # Adquiere el semáforo para limitar el número de conexiones simultaneas
            threading.Thread(target=self._atender_jugador, args=(jugador,)).start() # Crea un hilo para atender al jugador
        
    def _atender_jugador(self, jugador): # Método para atender a un jugador
        print(f"[Servidor] Atendiendo a Jugador {jugador.id_jugador} (Premium: {jugador.es_premium})")
        time.sleep(random.uniform(0.5, 1.5)) # Simula el tiempo de atención al jugador
        
        with self.lock: # Bloquea el acceso a la lista de jugadores conectados
            self.jugadores_conectados.append(jugador.id_jugador) # Agrega el jugador a la lista de jugadores conectados
            print(f"[Servidor] Jugador {jugador.id_jugador} conectado exitosamente.")
            
        self.semaforo.release() # Libera el semáforo
