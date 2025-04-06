#Versión 2.0
#Esta versión incluye la sincronización para evitar condiciones de carrera.

import threading

class Servidor: #Clase que representa al servidor
    def __init__(self): # Constructor de la clase
        self.jugadores_conectados = [] # Lista para almacenar los jugadores conectados
        self.lock = threading.Lock() # Lock para sincronizar el acceso a la lista de jugadores conectados

    def procesar_conexion(self, id_jugador): # Método para procesar la conexión de un jugador
        print(f"[Servidor] Procesando conexión de jugador {id_jugador}.") # Simula el procesamiento de la conexión
        
        with self.lock: # Bloquea el acceso a la lista de jugadores conectados
            self.jugadores_conectados.append(id_jugador) # Agrega el jugador a la lista de jugadores conectados
            print(f"[Servidor] Jugador: {id_jugador} conectado exitosamente.") # Indica que el jugador se ha conectado exitosamente
