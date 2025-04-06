class Servidor: #Clase que representa al servidor
    def __init__(self): # Constructor de la clase
        self.jugadores_conectados = [] # Lista para almacenar los jugadores conectados

    def procesar_conexion(self, id_jugador): # Método para procesar la conexión de un jugador
        print(f"[Servidor] Procesando conexión de jugador {id_jugador}.") # Simula el procesamiento de la conexión
        #Aqui agregarémos la sincronización en el futuro
        self.jugadores_conectados.append(id_jugador) # Agrega el jugador a la lista de jugadores conectados
        print(f"[Servidor] Jugador: {id_jugador} conectado exitosamente.") # Indica que el jugador se ha conectado exitosamente