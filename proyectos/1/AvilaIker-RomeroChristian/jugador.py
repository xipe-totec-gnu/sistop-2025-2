#Importaciones
import threading
import time
import random

class Jugador(threading.Thread): # Clase que representa a un jugador, hereda de threading.Thread
    def __init__(self, id_jugador, servidor):
        super().__init__() # Inicializa el hilo
        self.id_jugador = id_jugador # Identificador del jugador
        self.servidor = servidor # Referencia al servidor al que se conectará el jugador

    def run(self): # Método que se ejecutará cuando se inicie el hilo
        print(f"[Jugador {self.id_jugador}] Intentando conectarse al servidor...") # Simula la conexión al servidor
        time.sleep(random.uniform(0.1, 1.0)) # Simula el tiempo de conexión

        #Aqui se conecta al servidor
        self.servidor.procesar_conexion(self.id_jugador) # Procesa la conexión en el servidor