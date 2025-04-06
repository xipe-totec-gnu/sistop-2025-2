#Versión 2.0

class Jugador: # Clase que representa a un jugador
    def __init__(self, id_jugador, servidor, es_premium=False):
        self.id_jugador = id_jugador # Identificador del jugador
        self.servidor = servidor # Referencia al servidor
        self.es_premium = es_premium # Indica si el jugador es premium o no

    def solicitar_conexion(self): # Método para solicitar la conexión al servidor
        self.servidor.agregar_a_cola(self) # Agrega el jugador a la cola de espera del servidor
