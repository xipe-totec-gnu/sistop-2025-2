#Este programa simula la conexión de varios jugadores a un servidor. Cada jugador se conecta de manera concurrente, y el servidor procesa cada conexión de manera sincronizada.
#Versión 1.0
#Esta primera versión aún no incluye la sincronización, y contiene solo la estructura básica del programa.
#Como la variable compartida no cuenta con protección, puede que se produzcan condiciones de carrera.

#Faltan:
#Incluir sincronización.
#Incluir interfaz gráfica.

#Importaciones
from servidor import Servidor
from jugador import Jugador

#Main
def main():
    servidor = Servidor() # Crea una instancia del servidor
    jugadores = [] # Lista para almacenar los hilos de los jugadores

    num_jugadores = 10 # Número de jugadores a simular

    for i in range(num_jugadores): # Crea y inicia los hilos de los jugadores
        jugador = Jugador(id_jugador=i+1, servidor=servidor) # Crea una instancia del jugador
        jugadores.append(jugador) # Agrega el jugador a la lista de jugadores
        jugador.start() # Inicia el hilo del jugador

    for jugador in jugadores: # Espera a que todos los hilos de los jugadores terminen
        jugador.join() # Espera a que el hilo del jugador termine

    print("\n=== Simulación finalizada ===") # Indica que la simulación ha finalizado
    print(f"Jugadores conectados: {servidor.jugadores_conectados}") # Muestra la lista de jugadores conectados

if __name__ == "__main__":
    main()