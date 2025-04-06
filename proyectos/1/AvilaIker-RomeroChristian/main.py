#Este programa simula la conexión de varios jugadores a un servidor. Cada jugador se conecta de manera concurrente, y el servidor procesa cada conexión de manera sincronizada.
#Versión 3.0

#Falta:
#Incluir interfaz gráfica.

#Importaciones
from servidor import Servidor
from jugador import Jugador
import random

#Main
def main():
    servidor = Servidor(max_conexiones=3) # Crea una instancia del servidor
    jugadores = [] # Lista para almacenar los hilos de los jugadores

    num_jugadores = 10 # Número de jugadores a simular

    for i in range(num_jugadores): # Crea y inicia los hilos de los jugadores
        es_premium = random.choice([True, False]) # Determina aleatoriamente si el jugador es premium o no
        jugador = Jugador(id_jugador=i+1, servidor=servidor, es_premium=es_premium) # Crea una instancia del jugador
        jugadores.append(jugador) # Agrega el jugador a la lista de jugadores
        jugador.solicitar_conexion() # Solicita la conexión del jugador al servidor

    print("\n[Servidor] Iniciando procesamiento de conexiones...\n")
    servidor.procesar_conexiones() # Procesa las conexiones de los jugadores

if __name__ == "__main__":
    main()
