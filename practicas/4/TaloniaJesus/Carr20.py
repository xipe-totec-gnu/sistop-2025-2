##Este programa simula el juego 'carrera a 20' que se usa para hacer que los niños pequeños practiquen las cuentas mentales,
#pero en lugar de niños, se usan hilos

import threading
import random
import time

# Variables compartidas
cont = 0
meta = 20
lock = threading.Lock()
juego_terminado = False

def jugador(nombre):
    global cont, juego_terminado
    while not juego_terminado:
        time.sleep(random.uniform(0.1, 0.4))  # Simula una reacción entre 0.1 y 0.4 s
        avance = random.randint(1, 3)         # Simula una selección aleatoria de un número para sumar
        with lock:
            if juego_terminado:
                break
            cont += avance
            print(f"{nombre} avanza {avance} pasos. Total: {cont}")
            if cont == meta:
                print(f"\n{nombre} ha ganado la carrera llegando a {cont}")
                juego_terminado = True
            elif cont > meta:
                print(f"\n{nombre} ha ganado la carrera, pero se pasó de 20 por {cont-meta}" )
                juego_terminado = True

# Crear los hilos (jugadores)
hilo1 = threading.Thread(target=jugador, args=("Jugador 1",))
hilo2 = threading.Thread(target=jugador, args=("Jugador 2",))

print("¡Empieza la carrera a 20!\n")
hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

print("\n Carrera terminada.")
