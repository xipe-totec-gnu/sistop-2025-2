#Versión 3.0
#Esta versión incluye semáforos para limitar el número de conexiones simultaneas.

import threading
import time
import random

class Servidor: #Clase que representa al servidor
    def __init__(self, max_conexiones = 3): # Constructor de la clase
        self.jugadores_conectados = [] # Lista para almacenar los jugadores conectados
        self.lock = threading.Lock() # Lock para sincronizar el acceso a la lista de jugadores conectados
        self.semaforo = threading.Semaphore(max_conexiones) # Semaforo para limitar el número de conexiones simultaneas

    def procesar_conexion(self, id_jugador): # Método para procesar la conexión de un jugador
        print(f"[Servidor] Jugador {id_jugador} esperando su turno...") # Simula el procesamiento de la conexión

        self.semaforo.acquire() # Adquiere el semáforo para limitar el número de conexiones simultaneas
        print(f"[Servidor] Jugador {id_jugador} está siendo atendido...")

        try:
            time.sleep(random.uniform(0.1, 1.0)) # Simula el tiempo de procesamiento de la conexión
        
            with self.lock: # Bloquea el acceso a la lista de jugadores conectados
                self.jugadores_conectados.append(id_jugador) # Agrega el jugador a la lista de jugadores conectados
                print(f"[Servidor] Jugador: {id_jugador} conectado exitosamente.") # Indica que el jugador se ha conectado exitosamente
        finally:
            self.semaforo.release() # Libera el semáforo
            print(f"[Servidor] Jugador {id_jugador} ha terminado su conexión.")
